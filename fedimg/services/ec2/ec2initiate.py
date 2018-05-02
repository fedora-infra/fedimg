# -*- coding: utf-8 -*-
# This file is part of fedimg.
# Copyright (C) 2014-2018 Red Hat, Inc.
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
I don't know what to write here for documentation
"""

import logging
import os
import shutil

from itertools import product as itertools_product

import fedimg.messenger

from fedimg.config import AWS_VOLUME_TYPES, AWS_BASE_REGION
from fedimg.config import AWS_ROOT_VOLUME_SIZE
from fedimg.exceptions import SourceNotFound, CommandRunFailed
from fedimg.exceptions import UnCompressFailed
from fedimg.services.ec2.ec2imguploader import EC2ImageUploader
from fedimg.services.ec2.ec2imgpublisher import EC2ImagePublisher
from fedimg.utils import get_virt_types_from_url, get_source_from_image
from fedimg.utils import unxz_source_file
from fedimg.utils import get_image_name_from_image, get_file_arch
from fedimg.utils import get_image_name_from_ami_name_for_fedmsg

_log = logging.getLogger(__name__)


def main(image_urls, access_id, secret_key, regions, volume_types=None,
         volume_via_s3=True, ex_virt_types=None, push_notifications=False,
         compose_id=None):
    """
    The `ec2.ec2initiate.main` function iterates over the image urls and start
    uploading the image to the specified regions. The `image_urls`,
    `access_id`, and `regions` are the required params. `volume_types`,
    `ex_virt_types` are optional arguments, if not passed the values are picked
    up from the fedimg configuration.
    `volume_via_s3`, `push_notifications`, and `compose_id` are optional params
    with default values.

    Args:
        image_urls (list): List of the image urls to create AMIs. (reques
        access_id (str): AWS EC2 access id
        secret_key (str): AWS_EC2 secret key
        regions (list): List of AWS regions the AMI to be uploaded.
        volume_types (list): List of supported volumes for the AMIs to
            be created.
        volume_via_s3 (bool): If `True`, the images are uploaded via s3 method
            else using creating builder instances.
        ex_virt_types (list): List of the supported virts for the AMIs to
            be created.
        push_notifications (bool): If `True` the messages will be pushed to
            fedmsg, else skipped.
        compose_id: id of the current compose in process.
    """

    root_volume_size = AWS_ROOT_VOLUME_SIZE
    published_images = []

    if volume_types is None:
        volume_types = AWS_VOLUME_TYPES

    if regions is None:
        regions = [AWS_BASE_REGION]

    for image_url in image_urls:

        xz_file_path = None
        source = None

        # If the virt types is not provided then select the supported virt
        # types from the image.
        if ex_virt_types is None:
            virt_types = get_virt_types_from_url(image_url)
        else:
            virt_types = ex_virt_types

        try:
            xz_file_path = get_source_from_image(image_url)
            source = unxz_source_file(xz_file_path)

            image_architecture = get_file_arch(image_url)

            uploader = EC2ImageUploader(
                compose_id=compose_id,
                access_key=access_id,
                secret_key=secret_key,
                root_volume_size=root_volume_size,
                image_architecture=image_architecture,
                volume_via_s3=volume_via_s3,
                push_notifications=push_notifications,
                image_url=image_url
            )

            publisher = EC2ImagePublisher(
                compose_id=compose_id,
                access_key=access_id,
                secret_key=secret_key,
                push_notifications=push_notifications,
                image_url=image_url
            )

            combinations = itertools_product(
                    *[regions, virt_types, volume_types])
            for region, virt_type, volume_type in combinations:
                uploader.set_region(region)
                _log.info('Region is set to: %r' % region)

                uploader.set_image_virt_type(virt_type)
                _log.info('Virtualization type is set to: %r' % virt_type)

                image_name = get_image_name_from_image(
                    image_url=image_url,
                    virt_type=virt_type,
                    region=region,
                    volume_type=volume_type
                )
                uploader.set_image_name(image_name)
                _log.info('Image name is set to: %r' % image_name)

                uploader.set_image_volume_type(volume_type)
                _log.info('Volume type is set to: %r' % volume_type)

                uploader.set_availability_zone_for_region()

                if push_notifications:
                    fedimg.messenger.notify(
                        topic='image.upload',
                        msg=dict(
                            image_url=image_url,
                            image_name=get_image_name_from_ami_name_for_fedmsg(image_name),
                            destination=region,
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

                published_images.extend(publisher.publish_images(
                    region_image_mapping=[(region, image.id)]
                ))
        except CommandRunFailed:
            _log.error("Could not execute the command for the requested "
                       "image_url: %r" % image_url)
        except SourceNotFound:
            _log.error("Could not find the source for the requested image_url"
                       " : %r" % image_url)
        except UnCompressFailed:
            _log.error("Could not uncompress the request image: %r" %
                       image_url)
        except Exception as e:
            _log.error(e.message)
        finally:
            if xz_file_path:
                xz_file_dirname = os.path.dirname(xz_file_path)
                shutil.rmtree(xz_file_dirname)
                _log.info("Cleaned up %r" % xz_file_dirname)

    return published_images
