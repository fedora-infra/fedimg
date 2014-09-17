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

        # create image from offical Fedora image on Rackspace

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
