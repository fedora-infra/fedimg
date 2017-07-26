# This file is part of fedimg.
# Copyright (C) 2014-2017 Red Hat, Inc.
#
# fedimg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# fedimg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

import logging
log = logging.getLogger("fedmsg")

import multiprocessing.pool

import fedmsg.consumers
import fedmsg.encoding
import fedfind.release

import fedimg.uploader

from fedimg.config import PROCESS_COUNT, STATUS_FILTER
from fedimg.utils import get_rawxz_urls, get_value_from_dict


class FedimgConsumer(fedmsg.consumers.FedmsgConsumer):
    """ Listens for image Koji task completion and sends image files
        produced by the child createImage tasks to the uploader. """
    topic = ['org.fedoraproject.prod.pungi.compose.status.change']
    config_key = "fedimgconsumer.prod.enabled"

    def __init__(self, *args, **kwargs):
        super(FedimgConsumer, self).__init__(*args, **kwargs)

        # Threadpool for upload jobs
        self.upload_pool = multiprocessing.pool.ThreadPool(
            processes=PROCESS_COUNT
        )
        log.info("Super happy fedimg ready and reporting for duty.")

    def consume(self, msg):
        """ This is called when we receive a message matching our topics. """
        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        msg_info = msg['body']['msg']
        if msg_info['status'] not in STATUS_FILTER:
            return

        location = msg_info['location']
        compose_id = msg_info['compose_id']
        compose_metadata = fedfind.release.get_release_cid(compose_id).metadata
        images_meta = get_value_from_dict(
            compose_metadata,
            'images',
            'payload',
            'images',
            'CloudImages',
            'x86_64'
        )

        if images_meta is None:
            log.debug('No compatible image found to process')
            return

        upload_urls = get_rawxz_urls(location, images_meta)
        if len(upload_urls) > 0:
            log.info("Start processing compose id: %s" % compose_id)
            fedimg.uploader.upload(
                pool=self.upload_pool,
                urls=upload_urls,
                compose_id=compose_id
            )


class FedimgStagingConsumer(FedimgConsumer):
    topic = ['org.fedoraproject.stg.pungi.compose.status.change']
    config_key = "fedimgconsumer.stg.enabled"


class FedimgDevConsumer(FedimgConsumer):
    topic = ['org.fedoraproject.dev.pungi.compose.status.change']
    config_key = "fedimgconsumer.dev.enabled"