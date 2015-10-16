#!/bin/env python
# -*- coding: utf8 -*-

""" Triggers an upload process with the specified raw.xz URL. Useful for
    manually triggering Fedimg jobs. """

import logging
import logging.config
import multiprocessing.pool
import sys

import fedmsg
import fedmsg.config

import fedimg
import fedimg.services
from fedimg.services.ec2 import EC2Service, EC2ServiceException
import fedimg.uploader
from fedimg.util import virt_types_from_url

if len(sys.argv) != 2:
    print 'Usage: trigger_upload.py <rawxz_image_url>'
    sys.exit(1)

logging.config.dictConfig(fedmsg.config.load_config()['logging'])
log = logging.getLogger('fedmsg')

# Patch libcloud to give it support for the ec2 eu-central-1 region
import fedimg.haxx
fedimg.haxx.monkeypatch_libcloud()

upload_pool = multiprocessing.pool.ThreadPool(processes=4)

url = sys.argv[1]

fedimg.uploader.upload(upload_pool, [url])
