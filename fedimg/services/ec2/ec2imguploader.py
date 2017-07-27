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

import fedimg.messenger

from fedimg.utils import external_run_command, get_item_from_regex
from fedimg.services.ec2.ec2base import EC2Base


class EC2ImageUploader(EC2Base):
    """ Comment goes here """

    def __init__(self, *args, **kwargs):
        defaults = {
            'access_key': None,
            'image_name': 'Fedora-AMI',
            'image_description': 'Fedora AMI Description',
            'image_virtualization_type': 'hvm',
            'image_volume_type': 'gp2',
            'image_format': 'raw',
            'region': None,
            'secret_key': None,
            's3_bucket_name': 'Fedora-S3-Bucket',
            'volume_via_s3': True,
            'push_notifications': False, 
        }

        for (prop, default) in defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))

    def _determine_root_device_name(self):
        root_device_name = '/dev/sda'
        if self.image_virt_type == 'hvm':
            root_device_name = '/dev/sda1'

        log.debug('Root device name is set to %r for %r' % (
            root_device_name, self.image_virt_type))

        return root_device_name

    def _create_block_device_map(self, snapshot):
        root_device_name = self._determine_root_device_name()
        block_device_map = {
            'DeviceName': root_device_name,
            'Ebs': {
                'SnapshotId': snapshot.id,
                'VolumeSize': self.root_volume_size,
                'VolumeType': self.image_volume_type,
                'DeleteOnTermination': True,
            }
        }

        log.debug('Block device map created for %s' % snapshot.id)

        return [block_device_map]

    def _retry_and_get_volume_id(self, task_id):
        while True:
            output, err, retcode = external_run_command([
                'euca-describe-conversion-tasks',
                task_id,
                '--region',
                self.region
            ])

            if 'completed' in output:
                log.debug('Task %r complete. Fetching volume id...' % task_id)
                match = re.search('\s(vol-\w{17})', output)
                volume_id = match.group(1)

                log.debug('The id of the created volume: %r' % volume_id)

                return volume_id

            log.debug('Failed to find complete. Task %r still running. '
                      'Sleeping for 10 seconds.' % task_id)

    def get_volume_from_volume_id(self, volume_id):
        """ Comment goes here
        """
        #FIXME: This is not a optimized way of get all the volumes. Rather
        # send a patch to libcloud to filter the volume based on the volume_id

        volumes = self._connect().list_volumes()

        for volume in volumes:
            if volume.id == volume_id:
                return volume

    def _create_volume(self, source):
        if self.volume_via_s3:
            output, err, retcode = external_run_command([
                'euca-import-volume',
                source,
                '-f',
                self.image_format,
                '--region',
                self.region,
                '-b',
                self.s3_bucket_name,
                '-z',
                self.availability_zone
            ])

            log.debug('Initiate task to upload the image via S3. '
                      'Fetching task id...')

            task_id = get_item_from_regex(output, regex='\s(import-vol-\w{8})')
            log.info('Fetched task_id: %r. Listening to the task.' % task_id)

            volume_id = self._retry_and_get_volume_id(task_id)

            volume = self.get_volume_from_volume_id(volume_id)
            log.info('Finish fetching volume object using volume_id')

            return volume

    def _retry_and_get_snapshot(self, snapshot_id):

        #FIXME: Rather that listing all snapshot. Add a patch to libcloud to
        # pull the snapshot using the snapshot id.
        snapshots = self._connect().list_snapshots()
        for snapshot in snapshots:
            if snapshot.id == snapshot_id:
                break

        while snapshot['extra'] != 'completed':
            snapshots = self._connect().list_snapshots()
            for snapshot in snapshots:
                if snapshot.id == snapshot_id:
                    break

    def _create_snapshot(self, volume):
        snapshot_id = self._connect().create_volume_snapshot(
                volume=volume,
                name=self.snapshot_name
        )
        snapshot = self._retry_and_get_snapshot(snapshot_id)

        return snapshot

    def _register_image(self, snapshot):
        counter = 0
        block_device_map = self._create_block_device_map(snapshot)
        while True:
            if counter > 0:
                self.image_name = re.sub('\d(?!\d)',
                                         lambda x: str(int(x.group(0))+1),
                                         self.image_name)
            try:
                log.info('Registering the image in %r (snapshot id: %r) with '
                         'name %r' % (self.region, snapshot.id,
                                      self.image_name))
                image = self._connect().ex_register_image(
                    name=self.image_name,
                    description=self.image_description,
                    virtualization_type=self.virtualization_type,
                    architecture=self.image_architecture,
                    block_device_mapping=block_device_map)

                if self.push_notifications:
                    fedimg.messenger.notify(
                        topic='image.upload',
                        msg=dict(
                            image_url=self.image_url,
                            image_name=self.image_name,
                            destination=self.region,
                            service=self.service,
                            status='completed',
                            compose=self.compose_id,
                            extra=dict(
                                id=image.id,
                                virt_type=self.image_virtualization_type,
                                vol_type=self.image_volume_type
                            )
                        )
                    )

                return image

            except Exception as e:
                log.info('Could not register with name: %r' % self.image_name)
                if 'InvalidAMIName.Duplicate' in str(e):
                    counter = counter + 1
                else:
                    raise

    def _remove_volume(self, volume):
        log.info('[CLEAN] Destroying volume: %r' % volume.id)
        self._connect().destroy_volume(volume)

    def _clean_up(self):
        pass

    def create_volume(self, source):
        log.info('Start creating the volume from source: %r' % source)
        return self._create_volume(source)

    def create_snapshot(self, source):
        volume = self._create_volume(source)

        log.info('Start creating snapshot from volume: %r' % volume.id)
        snapshot = self._create_snapshot(volume)

        self._remove_volume(volume)

        return snapshot

    def register_image(self, snapshot):
        image = self._register_image(snapshot)

        return image

    def create_image(self, source):

        snapshot = self.create_snapshot(source)
        log.debug('Finished create snapshot: %r' % snapshot.id)

        log.info('Start to register the image '
                 'from the snapshot: %r' % snapshot.id)
        image = self.register_image(snapshot)
        log.debug('Finish registering the image with id: %r' % image.id)

        return image
