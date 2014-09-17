import os
import subprocess

from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider, DeploymentException

import fedimg


class HPServiceException(Exception):
    """ Custom exception for HP. """
    pass


class HPService(object):
    """ A class for interacting with an HP connection. """

    def __init__(self):
        self.regions = ['region-b.geo-1']

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an image
        in each Rackspace region. """

        cls = get_driver(Provider.HPCLOUD)
        driver = cls(fedimg.HP_USER, fedimg.HP_PASSWORD,
                     tenant_name=fedimg.HP_TENANT,
                     region=self.regions[0])

        # create image from offical Fedora image on HP

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
