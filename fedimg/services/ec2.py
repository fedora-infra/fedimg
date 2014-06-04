#!/bin/env python
# -*- coding: utf8 -*-

import fedimg

EC2_REGIONS = [
    'EC2_AP_NORTHEAST',     # ap-northeast-1
    'EC2_AP_SOUTHEAST',     # ap-southeast-1
    'EC2_AP_SOUTHEAST2',    # ap-southeast-2
    'EC2_EU_WEST',          # eu-west-1
    'EC2_SA_EAST',          # sa-east-1
    'EC2_US_EAST',          # (no special ID listed)
    'EC2_US_WEST',          # us-west-1
    'EC2_US_WEST_OREGON',   # us-west-2
]


def upload(image):
    """ Takes an image file and registers it as an AMI in each
    EC2 region. """
    pass
