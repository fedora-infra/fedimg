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


class RackspaceServiceException(Exception):
    """ Custom exception for RackspaceService. """
    pass


class RackspaceService(object):
    """ A class for interacting with a Rackspace connection. """

    def __init__(self):

        self.regions = ['dfw', 'ord', 'iad', 'lon', 'syd', 'hkg']

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an image
        in each Rackspace region. """

        cls = get_driver(Provider.RACKSPACE)
        driver = cls(fedimg.RACKSPACE_USER, fedimg.RACKSPACE_API_KEY,
                     region=self.regions[0])

        # create image

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

        try:
            # Must be EBS-backed for AMI registration to work.
            # Username must be provided properly or paramiko will throw an
            # error saying "invalid DSA key" even if the key is valid, in the
            # case that the _username_ is not valid. see:
            # http://mail-archives.apache.org/mod_mbox/libcloud-users/
            #      201303.mbox/%3CCAJMHEm+ihtKWPJxLjKR9ro10X-VDNzcVMgc8jb6+
            #      VLiLF4kCUA@mail.gmail.com%3E
            node = driver.deploy_node(name=name, image=image, size=size,
                                      ssh_username='fedora',
                                      ssh_alternate_usernames=['root'],
                                      ssh_key=fedimg.AWS_KEYPATH,
                                      deploy=msd,
                                      ex_ebs_optimized=True,
                                      ex_security_groups=['ssh'],
                                      ex_blockdevicemappings=mappings)
        except DeploymentException as e:
            print "Problem deploying node: {}".format(e.value)
            print "Terminating instance."
            driver.destroy_node(e.node)

        # register that volume as an AMI, possibly after snapshotting it

        # emit a fedmsg, etc
