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

from itertools import product as itertools_product

from fedimg.services.ec2.config import ACCESS_ID, SECRET_KEY, REGIONS
from fedimg.services.ec2.config import VOLUME_TYPES, VOLUME_VIA_S3
from fedimg.services.ec2.ec2imguploader import EC2ImageUploader
from fedimg.services.ec2.ec2imgpublisher import EC2ImagePublisher
from fedimg.utils import get_virt_types_from_url, get_source_for_image


def main(image_url):
    access_id = ACCESS_ID
    secret_key = SECRET_KEY
    regions = REGIONS
    volume_types = VOLUME_TYPES
    volume_via_s3 = VOLUME_VIA_S3
    virt_types = get_virt_types_from_url(image_url)

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
        uploader.set_image_virt_type(virt_type)
        uploader.set_image_volume_type(volume_type)

        publisher.set_region(region)

        image = uploader.create_image(source)

        publisher.publish_images(image_ids=[image.id])
