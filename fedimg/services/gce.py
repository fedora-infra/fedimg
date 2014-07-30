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


class GCEServiceException(Exception):
    """ Custom exception for GCE. """
    pass


class GCEService(object):
    """ A class for interacting with a GCE connection. """

    def __init__(self):
        self.datacenters = ['us-central1-a']

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an image
        in each Rackspace region. """

        cls = get_driver(Provider.GCE)
        driver = cls(fedimg.GCE_EMAIL, fedimg.GCE_KEYPATH,
                     project=fedimg.GCE_PROJECT_ID,
                     datacenter=self.datacenters[0])

        # create image from offical Fedora image on GCE

        # deploy node
        name = 'fedimg AMI builder'
        # TODO: Make automatically-created /dev/sda be deleted on termination
        mappings = [{'VirtualName': None,
                     'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                             'VolumeType': 'standard',
                             'DeleteOnTermination': 'true'},
                     'DeviceName': '/dev/sdb'}]

        # register that volume as an image

        # emit a fedmsg, etc
