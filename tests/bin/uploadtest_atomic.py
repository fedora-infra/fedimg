#!/bin/env python
# -*- coding: utf8 -*-

""" Does a full, real-life upload process directly by skipping the
    consume process. For development testing, mostly."""

import fedmsg
import fedmsg.config
import fedimg
import fedimg.services
from fedimg.services.ec2 import EC2Service, EC2ServiceException
import fedimg.uploader
from fedimg.util import virt_types_from_url

import logging
import logging.config

logging.config.dictConfig(fedmsg.config.load_config()['logging'])
log = logging.getLogger('fedmsg')

url = 'http://download.fedoraproject.org/pub/fedora/linux/releases/21/Cloud/Images/x86_64/Fedora-Cloud-Atomic-20141203-21.x86_64.raw.xz'

fedimg.uploader.upload([url])
