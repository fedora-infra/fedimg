#!/bin/env python
# -*- coding: utf8 -*-

import os
import subprocess

from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

import fedimg


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
                    'ami': attrs[4]}
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

        ami = self.amis[0]  # DEBUG (us east x86_64)
        cls = get_driver(ami['prov'])
        driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

        # select the desired node attributes
        sizes = driver.list_sizes()
        size_id = 'm1.small'
        # check to make sure we have access to that size node
        size = [s for s in sizes if s.id == size_id][0]
        image = NodeImage(id=ami['ami'], name=None, driver=driver)

        # deploy node
        name = 'fedimg AMI builder'  # TODO: will add raw image title
        # TODO: Make automatically-created /dev/sda be deleted on termination
        mappings = [{'VirtualName': None,
                     'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                             'VolumeType': 'standard',
                             'DeleteOnTermination': 'true'},
                     'DeviceName': '/dev/sdb'}]

        # read in ssh key
        with open(fedimg.AWS_KEYPATH) as f:
            key_content = f.read()

        # Add key to authorized keys for root user
        step_1 = SSHKeyDeployment(key_content)

        # Add script for deploymentA
        script = "sudo curl {0} | xzcat > /dev/sdb".format(raw_url)
        step_2 = ScriptDeployment(script)

        # Create deployment object
        msd = MultiStepDeployment([step_1, step_2])

        # must be EBS-backed for AMI registration to work
        node = driver.deploy_node(name=name, image=image, size=size,
                                  ssh_key=fedimg.AWS_KEYPATH,
                                  deploy=msd,
                                  ex_ebs_optimized=True,
                                  ex_security_groups=['ssh'],
                                  ex_blockdevicemappings=mappings)

        # register that volume as an AMI, possibly after snapshotting it

        # emit a fedmsg, etc
