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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
#
"""
I don't know what to write here for documentation.
"""
import logging

from fedimg.config import AWS_BASE_REGION
from fedimg.services.ec2.ec2imgpublisher import EC2ImagePublisher

LOG = logging.getLogger(__name__)


def main(regions, access_id, secret_key, images=None,
         image_ids=None, push_notifications=False, compose_id=None):

    if images is None and image_ids is None:
        LOG.debug('Either images or image_ids is required')
        raise

    publisher = EC2ImagePublisher(
        compose_id=compose_id,
        access_key=access_id,
        secret_key=secret_key,
        push_notifications=True,
    )

    if image_ids is None and images is not None:
        image_ids = [image.id for image in images]

    for image_id in image_ids:
        copied_images = publisher.copy_images_to_regions(
            image_id=image_id,
            regions=regions,
            base_region=AWS_BASE_REGION)
        copied_images = [elem.values() for elem in copied_images]
        publisher.publish_images(region_image_mapping=copied_images)
