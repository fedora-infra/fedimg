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

import re

from time import sleep

from fedimg.utils import external_run_command, get_item_from_regex
from fedimg.services.ec2.ec2base import EC2Base


class EC2ImagePublisher(EC2Base):
    """ Comment goes here """

    def __init__(self, **kwargs):
        defaults = {
            'access_key': None,
            'image_id': None,
            'image_name': 'Fedora-AMI',
            'image_description': 'Fedora AMI Description',
            'region': None,
            'secret_key': None,
            'visibility': 'all',
            'push_notifications': False,
        }

        for (prop, default) in defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))

    def _retry_till_image_is_public(self, image):
        """ Comment goes here """

        driver = self._connect()

        is_image_public = False
        while True:
            try:
                is_image_public = driver.ex_modify_image_attribute(
                    image,
                    {'LaunchPermission.Add.1.Group': 'all'})
            except Exception as e:
                if 'InvalidAMIID.Unavailable' in str(e):
                    # The copy isn't completed yet, so wait for 20 seconds
                    # more.
                    sleep(20)
                    continue
            break

        return is_image_public

    def _retry_till_snapshot_is_public(self, snapshot):

        driver = self._connect()

        while True:
            is_snapshot_public = driver.ex_modify_snapshot_attribute(
                snapshot,
                {'CreateVolumePermission.Add.1.Group': 'all'})

            if is_snapshot_public:
                break

        return is_snapshot_public

    def _generate_dummy_snapshot_object(self, snapshot_id):

        driver = self._connect()

        snapshot_obj = type('', (), {})()
        snapshot_obj.id = snapshot_id
        snapshot = driver.list_snapshots(snapshot=snapshot_obj)

        return snapshot

    def get_snapshot_from_image_id(self, image):
        """ Comment goes here """
        if isinstance(image, str):
            image_id = image
            image = self._connect().get_image(image_id)

        snapshot_id = image.extra['block_device_mapping']['snapshot_id']
        snapshots = self._connect().list_snapshots()
        for snapshot in snapshots:
            if snapshot.id == snapshot_id:
                return snapshot

    def publish_images(self, region_image_mapping=None):
        """ Comment goes here """

        published_images = []
        if region_image_mapping is None:
            return published_images

        for region, image_id in region_image_mapping:

            image = self.get_image(image_ids=image_id)
            is_image_public = self._retry_till_image_is_public(image)

            snapshot = self.get_snapshot_from_image_id(image)
            is_snapshot_public = self._retry_till_snapshot_is_public(snapshot)

            published_images.append((
                image.id,
                is_image_public,
                snapshot.id,
                is_snapshot_public,
                self.region
            ))

        return published_images

    def copy_images_to_other_regions(self, image_id=None, regions=None):
        """ Comment goes here """

        if (image_id is None) or (regions is None):
            return

        counter = 0
        copied_images = []
        image = self._connect().get_image(ex_image_ids=image_id)
        if not image:
            return []

        for region in regions:
            self.set_region(region)

            while True:
                if counter > 0:
                    self.image_name = re.sub(
                        '\d(?!\d)',
                        lambda x: str(int(x.group(0))+1),
                        self.image_name
                    )
                try:
                    image = self._connect().copy_image(
                        image,
                        name=self.image_name,
                        description=self.image_description)

                    copied_images.append((region, image.id))
                    break

                except Exception as e:
                    log.info('Could not register'
                             ' with name: %r' % self.image_name)
                    if 'InvalidAMIName.Duplicate' in str(e):
                        counter = counter + 1
                    else:
                        raise

        return copied_images

    def deprecate_images(self, image_ids=None, snapshot_perm='all'):
        """ Comment goes here """

        if image_ids is None:
            return

    def delete_images(self, image_ids=None, snapshot_perm='all'):

        if image_ids is None:
            return
