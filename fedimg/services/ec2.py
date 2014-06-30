#!/bin/env python
# -*- coding: utf8 -*-

import os
import subprocess

from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider, DeploymentException

import fedimg
import fedimg.messenger
from fedimg.util import get_file_arch


class EC2ServiceException(Exception):
    """ Custom exception for EC2Service. """
    pass


class EC2Service(object):
    """ A class for interacting with an EC2 connection. """

    def __init__(self):
        # Will be a list of dicts. Dicts will contain AMI info.
        self.amis = list()

        for line in fedimg.AWS_AMIS.split('\n'):
            """ Each line in AWS_AMIS has pipe-delimited attributes at these indicies:
            0: region (ex. eu-west-1)
            1: OS (ex. Fedora)
            2: version (ex. 20)
            3: arch (i386 or x86_64)
            4: ami name (ex. ami-68e3d32d) """
            # strip line to avoid any newlines or spaces from sneaking in
            attrs = line.strip().split('|')
            info = {'region': attrs[0],
                    'prov': self._region_to_provider(attrs[0]),
                    'os': attrs[1],
                    'ver': attrs[2],
                    'arch': attrs[3],
                    'ami': attrs[4],
                    'aki': attrs[5]}
            self.amis.append(info)

    def _region_to_provider(self, region):
        """ Takes a region name (ex. 'eu-west-1') and returns
        the appropriate libcloud provider value. """
        providers = {'ap-northeast-1': Provider.EC2_AP_NORTHEAST,
                     'ap-southeast-1': Provider.EC2_AP_SOUTHEAST,
                     'ap-southeast-2': Provider.EC2_AP_SOUTHEAST2,
                     'eu-west-1': Provider.EC2_EU_WEST,
                     'sa-east-1': Provider.EC2_SA_EAST,
                     'us-east-1': Provider.EC2_US_EAST,
                     'us-west-1': Provider.EC2_US_WEST,
                     'us-west-2': Provider.EC2_US_WEST_OREGON}
        return providers[region]

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an AMI in each
        EC2 region. """

        node = None
        volume = None
        snapshot = None
        test_node = None
        build_name = 'Fedimg build'
        destination = 'somewhere'

        fedimg.messenger.message(build_name, destination, 'started')

        try:
            ami = self.amis[0]  # DEBUG (us east x86_64)
            cls = get_driver(ami['prov'])
            driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

            # select the desired node attributes
            sizes = driver.list_sizes()
            size_id = 'm1.large'
            # check to make sure we have access to that size node
            size = [s for s in sizes if s.id == size_id][0]
            image = NodeImage(id=ami['ami'], name=None, driver=driver)

            # deploy node
            name = 'fedimg AMI builder'  # TODO: will add raw image title
            # TODO: Make automatically-created /dev/sda be deleted
            # on termination
            mappings = [{'VirtualName': None,  # cannot specify with Ebs
                         'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                                 'VolumeType': 'standard',
                                 'DeleteOnTermination': 'false'},
                         'DeviceName': '/dev/sdb'}]

            # read in ssh key
            with open(fedimg.AWS_PUBKEYPATH, 'rb') as f:
                key_content = f.read()

            # Add key to authorized keys for root user
            step_1 = SSHKeyDeployment(key_content)

            # Add script for deployment
            # Device becomes /dev/xvdb on instance due to recent kernel change
            script = "curl {0} | sudo xzcat > /dev/xvdb".format(raw_url)
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            # Fedmsg info
            file_name = raw_url.split('/')[-1]
            build_name = file_name.replace('.raw.xz', '')
            destination = 'EC2 ({region})'.format(region=ami['region'])

            # Must be EBS-backed for AMI registration to work.
            node = driver.deploy_node(name=name, image=image, size=size,
                                      ssh_username='fedora',
                                      ssh_alternate_usernames=['root'],
                                      ssh_key=fedimg.AWS_KEYPATH,
                                      deploy=msd,
                                      kernel_id=ami['aki'],
                                      ex_keyname=fedimg.AWS_KEYNAME,
                                      ex_security_groups=['ssh'],
                                      ex_ebs_optimized=True,
                                      ex_blockdevicemappings=mappings)

            # Temporary hack to let the deploy script run
            from time import sleep
            sleep(300)  # give it 5 minutes
            print "5 minutes have passed. Snapshotting and registering."

            # Terminate the utility instance
            driver.destroy_node(node)

            # Take a snapshot of the volume the image was written to
            volume = [v for v in driver.list_volumes()][0]  # DEBUG
            snapshot = driver.create_volume_snapshot(volume,
                                                     name='fedimg snap')
            snap_id = str(snapshot.id)

            # Delete the volume now that we've got the snapshot
            driver.destroy_volume(volume)

            # Block device mapping for the AMI
            mapping = [{'DeviceName': '/dev/sda',
                        'Ebs': {'SnapshotId': snap_id}}]

            # Actually register image
            # TODO: Perhaps generate a description?
            arch = get_file_arch(file_name)
            image = driver.ex_register_image(build_name,
                                             description=None,
                                             root_device_name='/dev/sda',
                                             block_device_mapping=mapping,
                                             architecture=arch)

            # Spin up a node of the AMI to test
            # TODO: Need to report back status of tests for this to be useful

            # Add script for deployment
            # Device becomes /dev/xvdb on instance due to recent kernel change
            script = fedimg.AWS_TEST
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            test_node = driver.deploy_node(name=name, image=image, size=size,
                                           ssh_username='fedora',
                                           ssh_alternate_usernames=['root'],
                                           ssh_key=fedimg.AWS_KEYPATH,
                                           deploy=msd,
                                           ex_keyname=fedimg.AWS_KEYNAME,
                                           ex_security_groups=['ssh'],
                                           ex_ebs_optimized=True)

            # TODO: Wait until script completes and fedmsg is emitted.

            # Destroy the test node
            driver.destroy_node(test_node)

            # TODO: Make sure the node's volume is also deleted

        except DeploymentException as e:
            fedimg.messenger.message(build_name, destination,
                                     'failed')
            print "Problem deploying node: {}".format(e.value)
            print "Terminating instance."
            driver.destroy_node(e.node)

        except Exception:
            fedimg.messenger.message(build_name, destination,
                                     'failed')
            print "Unexpected problem registering AMI."
            print "Terminating instance and destroying other resources."

            if node:
                driver.destroy_node(node)
            if volume:
                driver.destroy_volume(volume)
            if snapshot:
                driver.destroy_volume_snapshot(snapshot)
            if test_node:
                driver.destroy_node(test_node)

        # Emit success fedmsg
        fedimg.messenger.message(build_name, destination,
                                 'completed')
