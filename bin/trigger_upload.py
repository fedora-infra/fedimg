#!/bin/env python
# -*- coding: utf8 -*-
""" Triggers an upload process with the specified raw.xz URL. """

import logging
import logging.config
import multiprocessing.pool
import sys

import fedmsg.config
import fedimg.uploader

if len(sys.argv) != 3:
    print 'Usage: trigger_upload.py <rawxz_image_url> <compose_id>'
    sys.exit(1)

logging.config.dictConfig(fedmsg.config.load_config()['logging'])
log = logging.getLogger('fedmsg')

upload_pool = multiprocessing.pool.ThreadPool(processes=4)

url = sys.argv[1]
compose_id = sys.argv[2]

compose_meta = {
    'compose_id': compose_id
}

fedimg.uploader.upload(upload_pool, [url], compose_meta=compose_meta)
