#!/bin/env python
# -*- coding: utf8 -*-

import fedimg

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

EC2_REGIONS = [
    Provider.EC2_AP_NORTHEAST,     # ap-northeast-1
    Provider.EC2_AP_SOUTHEAST,     # ap-southeast-1
    Provider.EC2_AP_SOUTHEAST2,    # ap-southeast-2
    Provider.EC2_EU_WEST,          # eu-west-1
    Provider.EC2_SA_EAST,          # sa-east-1
    Provider.EC2_US_EAST,          # (no special ID listed)
    Provider.EC2_US_WEST,          # us-west-1
    Provider.EC2_US_WEST_OREGON,   # us-west-2
]


def upload(image):
    """ Takes a raw image file and registers it as an AMI in each
    EC2 region. """
    # TODO: Datatype check here to confirm that image is proper format (RAW)?
    for region in EC2_REGIONS:
        driver = get_driver(region)
        conn = driver(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)
