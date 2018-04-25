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
_log = logging.getLogger(__name__)

import re

import fedimg.messenger

from time import sleep

from fedimg.utils import external_run_command, get_item_from_regex
from fedimg.utils import get_image_name_from_ami_name_for_fedmsg
from fedimg.config import AWS_DELETE_RESOURCES, AWS_S3_BUCKET_NAME
from fedimg.services.ec2.ec2base import EC2Base


class EC2ImageUploader(EC2Base):
    """
    The 'ec2.ec2imguploader.EC2ImageUploader` creates the Amazon Machine Image
    (AMI) from the source.

    Args:
        access_key (str): Access key for the account.
        availability_zone (str): Availability zone to use
        compose_id (str): ID of the Compose
        image_name (str): Name of the Image
        image_description (str): Description of the image
        image_virtualization_type (str): Virtulization Type of the Image
        image_architecture (str): Architecture of the Image
        image_url (str): URL of the the Image
        image_volume_type (str): Volume Type of the Image
        image_format (str): Format of the Image
        region (str): Region to upload
        service (str): Name of the Fedimg service.
        secret_key (str): Secret Key for the account
        s3_bucket_name (str): Name of the S3 bucket
        volume_via_s3 (bool): Bool to control AMI using S3-method
        root_volume_size (str): Size of the AWS volume
        push_notifications (bool): Push notifications to fedmsg
    """

    def __init__(self, *args, **kwargs):
        defaults = {
            'access_key': None,
            'availability_zone': None,
            'compose_id': None,
            'image_name': 'Fedora-AMI',
            'image_description': 'Fedora AMI Description',
            'image_virtualization_type': 'hvm',
            'image_architecture': 'x86_64',
            'image_url': None,
            'image_volume_type': 'gp2',
            'image_format': 'raw',
            'region': None,
            'service': 'EC2',
            'secret_key': None,
            's3_bucket_name': AWS_S3_BUCKET_NAME,
            'volume_via_s3': True,
            'root_volume_size': 7,
            'push_notifications': False,
        }

        for (prop, default) in defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))

    def _determine_root_device_name(self):
        root_device_name = '/dev/sda'
        if self.image_virtualization_type == 'hvm':
            root_device_name = '/dev/sda1'

        _log.debug('Root device name is set to %r for %r' % (
            root_device_name, self.image_virtualization_type))

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

        _log.debug('Block device map created for %s' % snapshot.id)

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
                _log.debug('Task %r complete. Fetching volume id...' % task_id)
                match = re.search('\s(vol-\w{17})', output)
                volume_id = match.group(1)

                _log.debug('The id of the created volume: %r' % volume_id)

                return volume_id

            _log.debug('Failed to find complete. Task %r still running. '
                      'Sleeping for 10 seconds.' % task_id)
            sleep(10)

    def _create_snapshot(self, volume):
        snapshot = self._connect().create_volume_snapshot(
                volume=volume,
                name=self.image_name
        )
        snapshot_id = snapshot.id
        snapshot = self._retry_and_get_snapshot(snapshot_id)

        return snapshot

    def _retry_and_get_snapshot(self, snapshot_id):
        #FIXME: Rather that listing all snapshot. Add a patch to libcloud to
        # pull the snapshot using the snapshot id.
        snapshots = self._connect().list_snapshots()
        for snapshot in snapshots:
            if snapshot.id == snapshot_id:
                break

        while snapshot.extra['state'] != 'completed':
            snapshots = self._connect().list_snapshots()
            for snapshot in snapshots:
                if snapshot.id == snapshot_id:
                    break

        return snapshot

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

            if retcode != 0:
                _log.error('Unable to import volume. Out: %s, err: %s, ret: %s',
                          output,
                          err,
                          retcode)
                raise Exception('Creating the volume failed')

            _log.debug('Initiate task to upload the image via S3. '
                      'Fetching task id...')

            task_id = get_item_from_regex(output, regex='\s(import-vol-\w{8})')
            _log.info('Fetched task_id: %r. Listening to the task.' % task_id)

            volume_id = self._retry_and_get_volume_id(task_id)

            volume = self.get_volume_from_volume_id(volume_id)
            _log.info('Finish fetching volume object using volume_id')

            return volume

    def _register_image(self, snapshot):
        counter = 0
        block_device_map = self._create_block_device_map(snapshot)
        root_device_name = self._determine_root_device_name()
        while True:
            if counter > 0:
                self.image_name = re.sub('\d(?!\d)$',
                                         lambda x: str(int(x.group(0))+1),
                                         self.image_name)
            try:
                _log.info('Registering the image in %r (snapshot id: %r) with '
                         'name %r' % (self.region, snapshot.id,
                                      self.image_name))
                image = self._connect().ex_register_image(
                    name=self.image_name,
                    description=self.image_description,
                    virtualization_type=self.image_virtualization_type,
                    architecture=self.image_architecture,
                    block_device_mapping=block_device_map,
                    root_device_name=root_device_name,
                    ena_support=True
                )

                if self.push_notifications:
                    fedimg.messenger.notify(
                        topic='image.upload',
                        msg=dict(
                            image_url=self.image_url,
                            image_name=get_image_name_from_ami_name_for_fedmsg(self.image_name),
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
                _log.info('Could not register with name: %r' % self.image_name)
                if 'InvalidAMIName.Duplicate' in str(e):
                    counter = counter + 1
                else:
                    raise

    def _remove_volume(self, volume):
        _log.info('[CLEAN] Destroying volume: %r' % volume.id)
        self._connect().destroy_volume(volume)

    def clean_up(self, image_id, delete_snapshot=True, force=False):
        """
        Clean the resources created during the upload process

        Args:
            image_id (str): ID of the AMI
            delete_snapshot (bool): Bool to control snapshot deletion along
                                    with AMI.
            force: Override AWS_DELETE_RESOURCES config value

        Returns:
            Boolean: True, if resources are deleted else False
        """
        if not AWS_DELETE_RESOURCES and force:
            _log.info('Deleting resource is disabled by config.'
                     'Override by passing force=True.')
            return False

        if self.volume:
            self._connect().destroy_volume(self.volume)

        self._connect().deregister_image(
            image_id,
            delete_snapshot=delete_snapshot
        )

        return True

    def set_image_virt_type(self, virt_type):
        """
        Set the `image_virtualization_type` attribute of the `EC2ImageUploader`
        object.

        Args:
            virt_type (str): virtualization type to set for the object.
        """
        self.image_virtualization_type = virt_type

    def set_image_url(self, image_url):
        """
        Set the `image_url` attribute of the `EC2ImageUploader` object.

        Args:
            image_url (str): image_url to set for the object.
        """
        self.image_url = image_url

    def set_image_name(self, image_name):
        """
        Set the `image_name` attribute of the `EC2ImageUploader` object.

        Args:
            image_name (str): image_name to set for the object.
        """
        self.image_name = image_name

    def set_image_volume_type(self, volume_type):
        """
        Set the `volume_type` attribute of the `EC2ImageUploader` object.

        Args:
            volume_type (str): volume_type to set for the object.
        """
        self.image_volume_type = volume_type

    def get_volume_from_volume_id(self, volume_id):
        """ Get the `` object from the volume_id.

        Args:
            volume_id (str): volume_id for the `EC2ImageUploader` object
        """
        #FIXME: This is not a optimized way of get all the volumes. Rather
        # send a patch to libcloud to filter the volume based on the volume_id

        volumes = self._connect().list_volumes()

        for volume in volumes:
            if volume.id == volume_id:
                return volume

    def set_availability_zone_for_region(self):
        """
        Returns a availability zone for the region
        """
        self.availability_zone = self._connect().ex_list_availability_zones(
            only_available=True)[0].name

    def create_volume(self, source):
        """
        Create a AWS volume out of the given source file

        Args:
            source (str): File path of the source file
        """
        _log.info('Start creating the volume from source: %r' % source)
        return self._create_volume(source)

    def create_snapshot(self, source):
        """
        Creates a AWS snapshot out of the given source file

        Args:
            source (str): File path of the source file

        Returns:
            snapshot: `VolumeSnapshot` object
        """
        self.volume = self._create_volume(source)

        _log.info('Start creating snapshot from volume: %r' % self.volume.id)
        snapshot = self._create_snapshot(self.volume)

        self._remove_volume(self.volume)

        return snapshot

    def register_image(self, snapshot):
        """
        Register the image for the given `` object,

        Args:
            snapshot: `VolumeSnapshot` object

        Returns:
            image: `NodeImage` object
        """
        image = self._register_image(snapshot)

        return image

    def create_image(self, source):
        """
        Create Amazon machin image out of the given source

        Args:
            source (str): path of the source cloud image file.

        Returns:
            image: returns the `NodeImage` object.
        """

        snapshot = self.create_snapshot(source)
        _log.debug('Finished create snapshot: %r' % snapshot.id)

        _log.info('Start to register the image '
                 'from the snapshot: %r' % snapshot.id)
        image = self.register_image(snapshot)
        _log.debug('Finish registering the image with id: %r' % image.id)

        return image
