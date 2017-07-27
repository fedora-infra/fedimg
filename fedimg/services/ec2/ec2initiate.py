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

import fedimg.messenger

from fedimg.services.ec2.config import AWS_VOLUME_TYPES, BASE_REGION
from fedimg.services.ec2.ec2imguploader import EC2ImageUploader
from fedimg.services.ec2.ec2imgpublisher import EC2ImagePublisher
from fedimg.utils import get_virt_types_from_url, get_source_for_image
from fedimg.utils import get_image_name_for_image


def main(image_urls,
         access_id,
         secret_key,
         regions,
         volume_types=None,
         volume_via_s3=True,
         ex_virt_types=None,
         push_notifications=False,
         compose_id=None):

    if volume_types is None:
        volume_types = AWS_VOLUME_TYPES

    for image_url in image_urls:

        if ex_virt_types is None:
            virt_types = get_virt_types_from_url(image_url)
        else:
            virt_types = ex_virt_types

        source = get_source_for_image(image_url)
        image_name = get_image_name_for_image(image_url)

        uploader = EC2ImageUploader(
            image_name=image_name,
            access_key=access_id,
            secret_key=secret_key,
            volume_via_s3=volume_via_s3,
            push_notifications=True,
        )

        base_region = BASE_REGION
        combinations = itertools_product(*[virt_types, volume_types])
        for virt_type, volume_type in combinations:
            uploader.set_region(base_region)
            log.debug('(uploader) Region is set to: %r' % base_region)

            uploader.set_image_virt_type(virt_type)
            log.debug('(uploader) Virtualization type '
                      'is set to: %r' % virt_type)

            uploader.set_image_volume_type(volume_type)
            log.debug('(uploader) Volume type is set to: %r' % volume_type)

            if push_notifications:
                fedimg.messenger.notify(
                    topic='image.upload',
                    msg=dict(
                        image_url=image_url,
                        image_name=image_name,
                        destination=base_region,
                        service='EC2',
                        status='started',
                        compose=compose_id,
                        extra=dict(
                            virt_type=virt_type,
                            vol_type=volume_type
                        )
                    )
                )
            image = uploader.create_image(source)

        publisher = EC2ImagePublisher(
            access_key=access_id,
            secret_key=secret_key,
            push_notifications=True,
        )
        remaining_regions = set(regions) - set(base_region)
        copied_images = publisher.copy_images_to_other_regions(
            image_id=image.id,
            regions=remaining_regions)
        published_images = publisher.publish_images(
            region_image_mapping=copied_images)
