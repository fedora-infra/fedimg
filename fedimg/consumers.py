# This file is part of fedimg.
# Copyright (C) 2014 Red Hat, Inc.
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
#

import logging
log = logging.getLogger("fedmsg")

import multiprocessing.pool

import fedmsg.consumers
import fedmsg.encoding
import koji

import fedimg.uploader
from fedimg.util import get_rawxz_url


class KojiConsumer(fedmsg.consumers.FedmsgConsumer):
    """ Listens for image Koji task completion and sends image files
        produced by the child createImage tasks to the uploader. """
    # To my knowledge, all *image* builds appear under this
    # exact topic, along with scratch builds.
    topic = 'org.fedoraproject.prod.buildsys.task.state.change'
    config_key = 'kojiconsumer'

    def __init__(self, *args, **kwargs):
        super(KojiConsumer, self).__init__(*args, **kwargs)

        # threadpool for upload jobs
        self.upload_pool = multiprocessing.pool.ThreadPool(processes=4)

        log.info("Super happy fedimg ready and reporting for duty.")

    def _get_upload_urls(self, builds):
        """ Takes a list of koji createImage task IDs and returns a list of
        URLs to .raw.xz image files that should be uploaded. """

        for build in builds:
            log.info('Got Koji build {0}'.format(build))

        # Create a Koji connection to the Fedora Koji instance
        koji_session = koji.ClientSession(fedimg.KOJI_SERVER)

        rawxz_files = []  # list of full URLs of files

        # Get all of the .raw.xz URLs for the builds
        if len(builds) == 1:
            task_result = koji_session.getTaskResult(builds[0])
            url = get_rawxz_url(task_result)
            if url:
                rawxz_files.append(url)
        elif len(builds) >= 2:
            koji_session.multicall = True
            for build in builds:
                koji_session.getTaskResult(build)
            results = koji_session.multiCall()
            for result in results:
                if not result: continue
                url = get_rawxz_url(result[0])
                if url:
                    rawxz_files.append(url)

        # We only want to upload:
        # 64 bit: base, atomic, bigdata
        # Not uploading 32 bit, vagrant, experimental, or other images.
        upload_files = []  # files that will actually be uploaded
        for url in rawxz_files:
            u = url.lower()
            if u.find('x86_64') > -1 and u.find('vagrant') == -1:
                if (u.find('fedora-cloud-base') > -1
                        or u.find('fedora-cloud-atomic') > -1
                        or u.find('fedora-cloud-bigdata') > -1):
                    upload_files.append(url)
                    log.info('Image {0} will be uploaded'.format(url))

        return upload_files

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        # If the build method is "image", we check to see if the child
        # task's method is "createImage".
        if msg_info["method"] == "image":
            if isinstance(msg_info["children"], list):
                for child in msg_info["children"]:
                    if child["method"] == "createImage":
                        # We only care about the image if the build
                        # completed successfully (with state code 2).
                        if child["state"] == 2:
                            builds.append(child["id"])

        if len(builds) > 0:
            fedimg.uploader.upload(self.upload_pool,
                                   self._get_upload_urls(builds))
