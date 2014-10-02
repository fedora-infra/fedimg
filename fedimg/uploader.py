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

import koji

import fedimg
from fedimg.services.ec2 import EC2Service
from fedimg.util import get_rawxz_url


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """

    # Create a Koji connection to the Fedora Koji instance
    koji_session = koji.ClientSession(fedimg.KOJI_SERVER)

    upload_files = list()  # list of full URLs of files

    if len(builds) == 1:
        task_result = koji_session.getTaskResult(builds[0])
        upload_files.append(get_rawxz_url(task_result))
    elif len(builds) >= 2:
        # Right now, builds only produce one .raw.xz file, so this should
        # never happen.
        koji_session.multicall = True
        for build in builds:
            koji_session.getTaskResult(build)
        results = koji_session.multiCall()
        for result in results:
            upload_files.append(get_rawxz_url(result))

    logging.info('Starting upload process')

    # EC2 upload
    ec2 = EC2Service()
    for image in upload_files:
        # If the image is 32 bit and a base image
        # OR if it's 64 bit and an atomic or bigdata image,
        # then go ahead and upload the image
        if (image.find('i386') > -1
           and image.find('fedora-cloud-base') > -1) or \
           (image.find('x86_64') > -1
           and (image.find('fedora-cloud-atomic') > -1 or
                image.find('fedora-cloud-bigdata') > -1)):
            ec2.upload(image)
        else:
            logging.info('Image {0} will not be uploaded')

    logging.info('Upload process finished')
