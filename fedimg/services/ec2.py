#!/bin/env python
# -*- coding: utf8 -*-

import fedimg

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


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

    def upload(self, image):
        """ Takes a raw image file and registers it as an AMI in each
        EC2 region. """
        # TODO: Check here to confirm that image is proper format (RAW)?
        for ami in self.amis:
            driver = get_driver(ami['prov'])
            conn = driver(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)
            # WORK IN PROGRESS
