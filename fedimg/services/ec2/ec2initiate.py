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

import logging
log = logging.getLogger("fedmsg")

from itertools import product as itertools_product

from fedimg.services.ec2.config import AWS_VOLUME_TYPES
from fedimg.services.ec2.ec2imguploader import EC2ImageUploader
from fedimg.services.ec2.ec2imgpublisher import EC2ImagePublisher
from fedimg.utils import get_virt_types_from_url, get_source_for_image


def main(image_urls,
         access_id,
         secret_key,
         regions,
         volume_types=None,
         volume_via_s3=True,
         ex_virt_types=None):

    if volume_types is None:
        volume_types = AWS_VOLUME_TYPES

    for image_url in image_urls:

        if ex_virt_types is None:
            virt_types = get_virt_types_from_url(image_url)
        else:
            virt_types = ex_virt_types

        source = get_source_for_image(image_url)

        uploader = EC2ImageUploader(
                access_key=access_id,
                secret_key=secret_key,
                volume_via_s3=volume_via_s3)

        publisher = EC2ImagePublisher(
                access_key=access_id,
                secret_key=secret_key)

        combinations = itertools_product(*[regions, virt_types, volume_types])
        for region, virt_type, volume_type in combinations:
            uploader.set_region(region)
            log.debug('(uploader) Region is set to: %r' % region)

            uploader.set_image_virt_type(virt_type)
            log.debug('(uploader) Virtualization type is set to: %r' % virt_type)

            uploader.set_image_volume_type(volume_type)
            log.debug('(uploader) Volume type to: %r' % volume_type)

            publisher.set_region(region)
            log.debug('(publisher) Region is set to: %r' % region)

            image = uploader.create_image(source)

            publisher.publish_images(image_ids=[image.id])
