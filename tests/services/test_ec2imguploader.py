# This file is part of fedimg.
# Copyright (C) 2018 Red Hat, Inc.
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

import unittest
import mock
import pytest

from fedimg.services.ec2.ec2imguploader import EC2ImageUploader


class MockStorageVolume(object):

    def __init__(self, id, name, size):
        self.id = id
        self.name = name
        self.size = size


class MockVolumeSnapshot(object):

    def __init__(self, id, name, volume, size, extra={}):
        self.id = id
        self.volume = volume
        self.name = name
        self.size = size
        self.extra = extra


class MockNodeImage(object):

    def __init__(self, id, name, description, virtualization_type,
                 architecture, block_device_mapping, root_device_name,
                 ena_support):
        self.id = id
        self.name = name
        self.description = description
        self.virtualization_type = virtualization_type
        self.architecture = architecture
        self.block_device_mapping = block_device_mapping
        self.root_device_name = root_device_name
        self.ena_support = ena_support


class MockAvailabilityZone(object):

    def __init__(self, name, region_code):
        self.name = name
        self.region_code = region_code


class CallableExhausted(Exception):
    pass


class CallableLimiter(object):
    def __init__(self, limit):
        self.limit = limit
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls > self.limit:
            raise CallableExhausted


class TestEC2ImageUploader(unittest.TestCase):

    def setUp(self):
        self.ec2imgup_obj = EC2ImageUploader(
            access_key='ABCDEFGHIJKLMNO123456789',
            secret_key='THISISASECRETKEYWITH0987',
            image_virtualization_type='hvm',
            region='us-east-1',
            push_notifications=False,
        )

        self.ec2imgup_obj.set_image_name("Fedora Node Image")
        self.ec2imgup_obj.set_image_volume_type("gp2")
        self.ec2imgup_obj.set_image_url("http://somepage.org/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz")

    def test_determine_root_device_name(self):
        root_device_name = self.ec2imgup_obj._determine_root_device_name()

        self.assertEqual(root_device_name, '/dev/sda1')

    def test_determine_root_device_name_pv(self):
        self.ec2imgup_obj.set_image_virt_type('pv')
        root_device_name = self.ec2imgup_obj._determine_root_device_name()

        self.assertEqual(root_device_name, '/dev/sda')

    def test_create_block_device_map(self):
        self.ec2imgup_obj.set_image_virt_type('hvm')
        snapshot = type('Snapshot', (object,), {})()
        setattr(snapshot, 'id', 'snap-abcdefghijkelmnop098765')
        expected_block_device_map = {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'SnapshotId': 'snap-abcdefghijkelmnop098765',
                'VolumeSize': 7,
                'VolumeType': 'gp2',
                'DeleteOnTermination': True,
            }
        }

        block_device_map = self.ec2imgup_obj._create_block_device_map(snapshot)

        self.assertEqual([expected_block_device_map], block_device_map)

    @mock.patch('fedimg.services.ec2.ec2imguploader.external_run_command')
    def test_retry_and_get_volume_id_success(self, mock_external_run_command):
        mock_external_run_command.return_value = (
            """
TaskType        IMPORTVOLUME    TaskId  import-vol-fg695yoi     ExpirationTime  2018-04-04T20:53:53Z    Status  completed
DISKIMAGE       DiskImageFormat RAW     DiskImageSize   154979204 VolumeId        vol-04c07b599a3b3b051   VolumeSize      1        AvailabilityZone        us-east-1a      ApproximateBytesConverted    154979204""", "", 0)
        volume_id = self.ec2imgup_obj._retry_and_get_volume_id('import-vol-fg695yoi')
        self.assertEqual(volume_id, 'vol-04c07b599a3b3b051')

    @mock.patch('time.sleep', side_effect=CallableLimiter(2))
    @mock.patch('fedimg.services.ec2.ec2imguploader._log.debug')
    @mock.patch('fedimg.services.ec2.ec2imguploader.external_run_command')
    def test_retry_and_get_volume_id_failed(self, mock_external_run_command,
                                            mock_log, mock_time):
        mock_external_run_command.return_value = (
            """
TaskType        IMPORTVOLUME    TaskId  import-vol-fg695yoi     ExpirationTime  2018-04-04T20:53:53Z    Status  active  StatusMessage   Pending
DISKIMAGE       DiskImageFormat RAW     DiskImageSize   170793472       VolumeSize      1       AvailabilityZone        us-east-1a      ApproximateBytesConverted       0
154979204""", "", 0)

        with pytest.raises(CallableExhausted):
            self.ec2imgup_obj._retry_and_get_volume_id('import-vol-fg695yoi')
        mock_log.assert_called_with("Failed to find complete. Task "
                                    "'import-vol-fg695yoi' is still running. "
                                    "Sleeping for 10 seconds.")

    @mock.patch('fedimg.services.ec2.ec2imguploader._log.debug')
    @mock.patch('fedimg.services.ec2.ec2imguploader.external_run_command')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._retry_and_get_volume_id',
                return_value="vol-04c07b599a3b3b051")
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader.get_volume_from_volume_id')
    def test_create_volume(self, mock_get_volume_from_volume_id,
                           mock_retry_and_get_volume_id,
                           mock_run_external_command, mock_log):
        mock_run_external_command.return_value = (
            """
Uploading image for task import-vol-ffokhf75
Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz.part.0  ( 1/3) 100% |==========================================================================================================|  60.00 MB   8.03 MB/s Time: 0:00:01
Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz.part.1  ( 2/3) 100% |==========================================================================================================|  60.00 MB   4.35 MB/s Time: 0:00:02
Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz.part.2  ( 3/3) 100% |==========================================================================================================|  60.00 MB   4.35 MB/s Time: 0:00:02
TaskType        IMPORTVOLUME    TaskId  import-vol-ffokhf75     ExpirationTime  2018-04-10T14:26:15Z    Status  active  StatusMessage   Pending
DISKIMAGE       DiskImageFormat RAW     DiskImageSize   188743680       VolumeSize      1       AvailabilityZone        us-east-1a      ApproximateBytesConverted       0""", "", 0)
        mock_get_volume_from_volume_id.return_value = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )
        volume = self.ec2imgup_obj._create_volume('/tmp/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz')
        mock_log.has_calls([
            'Fetched task_id: import-vol-ffokhf75. Listening to the task.',
            'Finish fetching volume object using volume_id'
        ])
        self.assertEquals(volume.id, 'vol-04c07b599a3b3b051')

    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._retry_and_get_snapshot')
    @mock.patch('fedimg.services.ec2.ec2base.EC2Base._connect')
    def test_create_snapshot(self, mock_ec2base_connect,
                             mock_retry_and_get_snapshot):
        mock_volume = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )
        mock_snapshot = MockVolumeSnapshot(
            id='snap-yeu4uwj2jwk4456k9',
            volume=mock_volume,
            name='Fedora Volume Snapshot',
            size=7
        )
        mock_ec2base_connect.create_volume_snapshot = mock_snapshot
        # The method _retry_and_get_snapshots retries until the snapshot is
        # created and returns the same snapshot object. This method is a
        # utility to confirm to move forward only if the snapshot has been
        # created.
        mock_retry_and_get_snapshot.return_value = mock_snapshot

        snapshot = self.ec2imgup_obj._create_snapshot(mock_volume)
        self.assertEquals(snapshot.id, mock_snapshot.id)

    def test_retry_and_get_snapshot(self):
        mock_volume_1 = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )
        mock_volume_2 = MockStorageVolume(
            id='vol-04c07b599a3b3b052',
            name='Fedora-Volume',
            size=7
        )
        mock_snapshots = mock.PropertyMock(return_value=[
            MockVolumeSnapshot(
                id='snap-yeu4uwj2jwk4456k9',
                volume=mock_volume_1,
                name='Fedora Volume Snapshot',
                size=7,
                extra={
                    'state': 'completed'
                }
            ),
            MockVolumeSnapshot(
                id='snap-qwew332re32rfef45',
                volume=mock_volume_2,
                name='Fedora Volume Snapshot',
                size=7,
                extra={
                    'state': 'completed',
                }
            )
        ])

        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'list_snapshots', mock_snapshots)
        snapshot = self.ec2imgup_obj._retry_and_get_snapshot(
                'snap-yeu4uwj2jwk4456k9')

        self.assertEquals(snapshot.id, 'snap-yeu4uwj2jwk4456k9')

    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._create_block_device_map', return_value="")
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._determine_root_device_name', return_value="")
    def test_register_image(self, mock_create_blk_device_map,
            mock_root_device_map):
        self.ec2imgup_obj.image_name = 'Fedora Image Name'
        mock_image = mock.PropertyMock(return_value=MockNodeImage(
                id='ami-23e56tt',
                name='Fedora AMI',
                description='Fedora AMI',
                virtualization_type='hvm',
                architecture='x86_64',
                block_device_mapping={},
                root_device_name='/dev/sda1',
                ena_support=True
            )
        )
        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'ex_register_image', mock_image)

        mock_volume = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )
        mock_snapshot = MockVolumeSnapshot(
            id='snap-yeu4uwj2jwk4456k9',
            volume=mock_volume,
            name='Fedora Volume Snapshot',
            size=7
        )

        node_image = self.ec2imgup_obj._register_image(mock_snapshot)
        self.assertEqual(node_image.id, 'ami-23e56tt')

    @mock.patch("fedimg.services.ec2.ec2imguploader._log.info")
    def test_remove_volume(self, mock_log):
        mock_volume = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )
        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'destroy_volume',
                mock.PropertyMock(return_value=True))

        self.ec2imgup_obj._remove_volume(mock_volume)

        mock_log.assert_called_with("[CLEAN] Destroying volume: "
                                    "'vol-04c07b599a3b3b051'")

    def test_clean_up(self):
        mock_volume = MockStorageVolume(
            id='vol-04c07b599a3b3b051',
            name='Fedora-Volume',
            size=7
        )

        setattr(self.ec2imgup_obj, 'volume', mock_volume)
        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'destroy_volume',
                mock.PropertyMock(return_value=True))

        mock_image = mock.PropertyMock(return_value=MockNodeImage(
                id='ami-23e56tt',
                name='Fedora AMI',
                description='Fedora AMI',
                virtualization_type='hvm',
                architecture='x86_64',
                block_device_mapping={},
                root_device_name='/dev/sda1',
                ena_support=True
            )
        )
        setattr(self.ec2imgup_obj._connect(), 'get_image', mock_image)
        setattr(self.ec2imgup_obj._connect(), 'delete_image',
                mock.PropertyMock(return_value=True))

        is_clean_up_complete = self.ec2imgup_obj.clean_up('ami-23e56tt')

        self.assertTrue(is_clean_up_complete)

    def test_get_volume_from_volume_id(self):

        mock_volumes = mock.PropertyMock(return_value=[
            MockStorageVolume(
                id='vol-04c07b599a3b3b051',
                name='Fedora-Volume',
                size=7
            ),
            MockStorageVolume(
                id='vol-04c07b599a3b3b052',
                name='Fedora-Volume',
                size=7
            ),
        ])

        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'list_volumes', mock_volumes)

        volume = self.ec2imgup_obj.get_volume_from_volume_id('vol-04c07b599a3b3b051')

        self.assertEqual(volume.id, 'vol-04c07b599a3b3b051')

    @mock.patch('fedimg.services.ec2.ec2imguploader._log.info')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._create_volume')
    def test_main_create_volume(self, mock_create_volume, mock_log):
        mock_volume = MockStorageVolume(
                id='vol-04c07b599a3b3b051',
                name='Fedora-Volume',
                size=7
            ),
        mock_create_volume.return_volume = mock_volume

        self.ec2imgup_obj.create_volume('/tmp/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz')
        mock_log.assert_called_with("Start creating the volume from source: "
                                    "'/tmp/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz'")

    @mock.patch('fedimg.services.ec2.ec2imguploader._log.info')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._create_volume')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._create_snapshot')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._remove_volume')
    def test_main_create_snapshot(self, mock_remove_volume, mock_create_snapshot,
                                  mock_create_volume, mock_log):
        mock_volume = MockStorageVolume(
                id='vol-04c07b599a3b3b0TGG51',
                name='Fedora-Volume',
                size=7
            )
        mock_snapshot = MockVolumeSnapshot(
            id='snap-yeu4uwj2jwk4456k9',
            volume=mock_volume,
            name='Fedora Volume Snapshot',
            size=7
        )

        mock_create_volume.return_value = mock_volume
        mock_create_snapshot.return_value = mock_snapshot
        mock_remove_volume.return_value = True

        snapshot = self.ec2imgup_obj.create_snapshot('/tmp/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz')

        self.assertEqual(snapshot.id, 'snap-yeu4uwj2jwk4456k9')

    def test_set_availability_zone_for_region(self):
        mock_availability_zone = mock.PropertyMock(
            return_value=[
                MockAvailabilityZone(
                    name='us-east-1a',
                    region_code='us-east-1'
                ),
                MockAvailabilityZone(
                    name='us-east-1b',
                    region_code='us-east-1'
                )
            ]
        )

        setattr(self.ec2imgup_obj, '_connect', mock.MagicMock())
        setattr(self.ec2imgup_obj._connect(), 'ex_list_availability_zones',
                mock_availability_zone)

        self.ec2imgup_obj.set_availability_zone_for_region()

        self.assertEqual(self.ec2imgup_obj.availability_zone, 'us-east-1a')

    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader._register_image')
    def test_main_register_image(self, mock_register_image):
        mock_volume = MockStorageVolume(
                id='vol-04c07b599a3b3b051',
                name='Fedora-Volume',
                size=7
            )
        mock_snapshot = MockVolumeSnapshot(
            id='snap-yeu4uwj2jwk4456k9',
            volume=mock_volume,
            name='Fedora Volume Snapshot',
            size=7
        )

        mock_image = MockNodeImage(
                id='ami-23e56tt',
                name='Fedora AMI',
                description='Fedora AMI',
                virtualization_type='hvm',
                architecture='x86_64',
                block_device_mapping={},
                root_device_name='/dev/sda1',
                ena_support=True
            )

        mock_register_image.return_value = mock_image
        image = self.ec2imgup_obj.register_image(mock_snapshot)

        self.assertEqual(image.id, 'ami-23e56tt')

    @mock.patch('fedimg.services.ec2.ec2imguploader._log.debug')
    @mock.patch('fedimg.services.ec2.ec2imguploader._log.info')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader.create_snapshot')
    @mock.patch('fedimg.services.ec2.ec2imguploader.EC2ImageUploader.register_image')
    def test_main_create_image(self, mock_register_image,
            mock_create_snapshot, mock_info_log, mock_debug_log):
        mock_volume = MockStorageVolume(
                id='vol-04c07b599a3b3b051',
                name='Fedora-Volume',
                size=7
            )

        mock_snapshot = MockVolumeSnapshot(
            id='snap-yeu4uwj2jwk4456k9',
            volume=mock_volume,
            name='Fedora Volume Snapshot',
            size=7
        )

        mock_image = MockNodeImage(
                id='ami-23e56tt',
                name='Fedora AMI',
                description='Fedora AMI',
                virtualization_type='hvm',
                architecture='x86_64',
                block_device_mapping={},
                root_device_name='/dev/sda1',
                ena_support=True
            )

        mock_create_snapshot.return_value = mock_snapshot
        mock_register_image.return_value = mock_image

        image = self.ec2imgup_obj.create_image('/tmp/Fedora-Cloud-Base-28-20180403.n.0.x86_64.raw.xz')

        mock_info_log.assert_called_with("Start to register the image from the snapshot: 'snap-yeu4uwj2jwk4456k9'")
        mock_debug_log.has_calls([
            "Finished create snapshot: 'snap-yeu4uwj2jwk4456k9'",
            "Finish registering the image with id: 'ami-23e56tt'"]
        )

        self.assertEqual(image.id, 'ami-23e56tt')
