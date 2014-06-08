#!/bin/env python
# -*- coding: utf8 -*-

import fedimg

from libcloud.compute.base import NodeImage
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider


class EC2ServiceException(Exception):
    """ Custom exception for EC2Service. """
    pass


class EC2Service(object):
    """ A class for interacting with an EC2 connection. """

    # Will be a list of dicts. Dicts will contain AMI info.
    amis = list()

    def __init__(self):

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
        if region == 'ap-northeast-1' return Provider.EC2_AP_NORTHEAST
        if region == 'ap-southeast-1' return Provider.EC2_AP_SOUTHEAST
        if region == 'ap-southeast-2' return Provider.EC2_AP_SOUTHEAST2
        if region == 'eu-west-1' return Provider.EC2_EU_WEST
        if region == 'sa-east-1' return Provider.EC2_SA_EAST
        if region == 'us-east-1' return Provider.EC2_US_EAST
        if region == 'us-west-1' return Provider.EC2_US_WEST
        if region == 'us-west-2' return Provider.EC2_US_WEST_OREGON

        # If none of those returned, there is a problem.
        raise EC2ServiceException('Invalid region, no matching provider.')

    def upload(self, raw):
        """ Takes a raw image file and registers it as an AMI in each
        EC2 region. """
        # TODO: Check here to confirm that image is proper format (RAW)?
        # TODO: Make sure that once we create an AMI, we copy it to other
        # regions via region-to-region copy rather than remake the AMI
        # in each region (might just be copying image though).
        for ami in self.amis:
            cls = get_driver(ami['prov'])
            driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

            # select the desired node attributes
            sizes = driver.list_sizes()
            size_id = 't1.micro'  # The smallest one for now.
            # check to make sure we have access to that size node
            size = [s for s in sizes if s.id == size_id][0]
            image = NodeImage(id=ami['ami'], name=None, driver=driver)

            # create node
            # must be EBS-backed for AMI registration to work
            name = 'fedimg AMI builder'  # TODO: will add raw image title
            node = driver.create_node(name=name, image=image, size=size,
                                      ex_iamprofile=fedimg.AWS_IAM_PROFILE,
                                      ex_ebs_optimized=True)

            # create a volume for the uploaded image to be written to
            vol_name = 'fedimg AMI volume'  # TODO; will add raw image title
            # TODO: might need to provide availability zone in the below call
            vol = driver.create_volume(10, vol_name)  # new 10 GB volume

            # Attach the new volume to the node
            # TODO: Check to see if it's faster to have the second volume
            # in the block device mappings when the instance is spun up.
            driver.attach_volume(node, vol, device='/dev/sdb')


            # write image to secondary volume

            # register that volume as an AMI, possibly after snapshotting it

            # emit a fedmsg, etc
