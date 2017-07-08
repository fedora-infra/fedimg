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

from fedimg.utils import external_run_command, get_item_from_regex
from fedimg.ec2.ec2base import EC2Base


class EC2ImagePublisher(EC2Base):
    """ Comment goes here """

    def __init__(self, **kwargs):
        defaults = {
            'access_key': None,
            'image_id': None,
            'region': None,
            'secret_key': None,
            'visibility': 'all'
        }

        for (prop, default) in defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))

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

    def publish_images(self, image_ids=None):
        """ Comment goes here """
        driver = self._connect()
        images = driver.list_images(ex_image_ids=image_ids)

        for image in images:
            driver.ex_modify_image_attribute(image, {
                'LaunchPermission.Add.1.Group': 'all'})

            snapshot = self.get_snapshot_from_image_id(image.id)
            driver.ex_modify_snapshot_attribute(snapshot, {
                'CreateVolumePermission.Add.1.Group': 'all'})
