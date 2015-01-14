#!/bin/env python
# -*- coding: utf8 -*-

""" Does a full, real-life upload process directly by skipping the
    consume process. For development testing, mostly."""

import fedmsg
import fedimg
import fedimg.services
from fedimg.services.ec2 import EC2Service, EC2ServiceException
import fedimg.uploader
from fedimg.util import virt_types_from_url

import logging
logging.basicConfig()
log = logging.getLogger('fedmsg')
log.setLevel(logging.DEBUG)

url = 'http://download.fedoraproject.org/pub/fedora/linux/releases/21/Cloud/Images/x86_64/Fedora-Cloud-Base-20141203-21.x86_64.raw.xz'

fedimg.uploader.upload([url])
