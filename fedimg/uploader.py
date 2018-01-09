# -*- coding: utf-8 -*-
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
"""
This module checks for the active services (configured through the fedimg
configuration file) and call the main method for the service.
"""

import logging

from fedimg.config import ACTIVE_SERVICES
from fedimg.services.ec2.ec2initiate import main as ec2main
from fedimg.services.ec2.ec2copy import main as ec2copy
from fedimg.config import AWS_ACCESS_ID, AWS_SECRET_KEY
from fedimg.config import AWS_BASE_REGION, AWS_REGIONS


LOG = logging.getLogger(__name__)


def upload(pool, urls, *args, **kwargs):
    """
    Takes a list (urls) of one or more .raw.xz image files and
    sends them off to cloud services for registration. The upload
    jobs threadpool must be passed as `pool`.

    Args:
        pool (multithreading.pool.ThreadPool): The thread pool to parallelize
        the uploads.
        urls (list): List of cloud image urls.
    """

    active_services = ACTIVE_SERVICES
    compose_id = kwargs.get('compose_id')

    if 'aws' in active_services:
        LOG.info('Starting to process AWS EC2Service.')
        images_metadata = ec2main(
            urls,
            AWS_ACCESS_ID,
            AWS_SECRET_KEY,
            [AWS_BASE_REGION],
            compose_id=compose_id
        )
        for image_metadata in images_metadata:
            image_id = image_metadata['image_id']
            aws_regions = list(set(AWS_REGIONS) - set([AWS_BASE_REGION]))
            ec2copy(
                aws_regions,
                AWS_ACCESS_ID,
                AWS_SECRET_KEY,
                image_ids=[image_id],
                push_notifications=True,
                compose_id=compose_id
            )
        LOG.info('AWS EC2Service process is completed.')
