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
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

import mock
import unittest
import subprocess
import paramiko

import fedimg
import fedimg.utils


def mock_ssh_exception(*args, **kwargs):
    raise paramiko.SSHException("Could not connect")

class TestFedimgUtils(unittest.TestCase):

    class MockPopen(object):
        def __init(self):
            pass

        def communicate(self, input=None):
            pass

        @property
        def returncode(self):
            pass

    def test_get_file_arch_x86_64(self):
        filename = 'Fedora-Atomic-26-1.5.x86_64.raw.xz'
        arch = fedimg.utils.get_file_arch(filename)
        assert arch == 'x86_64'

    def test_get_file_arch_aarch64(self):
        filename = 'Fedora-Cloud-Base-26-1.5.aarch64.raw.xz'
        arch = fedimg.utils.get_file_arch(filename)
        assert arch == None

    def test_get_rawxz_urls(self):
        images = [
            {
                "arch": "x86_64",
                "format": "qcow2",
                "implant_md5": None,
                "mtime": 1499295621,
                "path": "CloudImages/x86_64/images/Fedora-Atomic-26-1.5.x86_64.qcow2",
                "size": 702779904,
                "subvariant": "Atomic",
                "type": "qcow2",
                "volume_id": None
            },
            {
                "arch": "x86_64",
                "format": "raw.xz",
                "implant_md5": None,
                "mtime": 1499295718,
                "path": "CloudImages/x86_64/images/Fedora-Atomic-26-1.5.x86_64.raw.xz",
                "size": 529608216,
                "subvariant": "Atomic",
                "type": "raw-xz",
                "volume_id": None
            },
            {
                "arch": "x86_64",
                "bootable": False,
                "disc_count": 1,
                "disc_number": 1,
                "format": "raw.xz",
                "implant_md5": None,
                "mtime": 1499291771,
                "path": "CloudImages/x86_64/images/Fedora-Cloud-Base-26-1.5.x86_64.raw.xz",
                "size": 154897200,
                "subvariant": "Cloud_Base",
                "type": "raw-xz",
                "volume_id": None
            },
            {
                "arch": "x86_64",
                "format": "vagrant-libvirt.box",
                "implant_md5": None,
                "mtime": 1499291717,
                "path": "CloudImages/x86_64/images/Fedora-Cloud-Base-Vagrant-26-1.5.x86_64.vagrant-libvirt.box",
                "size": 229231805,
                "subvariant": "Cloud_Base",
                "type": "vagrant-libvirt",
                "volume_id": None
            },
        ]

        urls = fedimg.utils.get_rawxz_urls('https://fedoraproject.org', images)
        atomic_url = 'https://fedoraproject.org/CloudImages/x86_64/images/Fedora-Atomic-26-1.5.x86_64.raw.xz'
        cloud_base_url = 'https://fedoraproject.org/CloudImages/x86_64/images/Fedora-Cloud-Base-26-1.5.x86_64.raw.xz'

        assert len(urls) == 2
        assert atomic_url in urls
        assert cloud_base_url in urls

    def test_get_rawxz_urls_empty(self):
        images = [
            {
                "arch": "x86_64",
                "format": "qcow2",
                "implant_md5": None,
                "mtime": 1499295621,
                "path": "CloudImages/x86_64/images/Fedora-Atomic-26-1.5.x86_64.qcow2",
                "size": 702779904,
                "subvariant": "Atomic",
                "type": "qcow2",
                "volume_id": None
            },
            {
                "arch": "x86_64",
                "format": "vagrant-libvirt.box",
                "implant_md5": None,
                "mtime": 1499291717,
                "path": "CloudImages/x86_64/images/Fedora-Cloud-Base-Vagrant-26-1.5.x86_64.vagrant-libvirt.box",
                "size": 229231805,
                "subvariant": "Cloud_Base",
                "type": "vagrant-libvirt",
                "volume_id": None
            },
        ]

        urls = fedimg.utils.get_rawxz_urls('https://somepage.org', images)
        self.assertEquals(urls, [])

    def test_get_virt_types_hvm_pv(self):
        url = 'https://somepage.org/Fedora-Cloud-Base-26-1.5.x86_64.raw.xz'
        vtypes = fedimg.utils.get_virt_types_from_url(url)
        assert vtypes == ['hvm', 'paravirtual']

    def test_get_virt_types_only_hvm(self):
        url = 'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz'
        vtypes = fedimg.utils.get_virt_types_from_url(url)
        assert vtypes == ['hvm']

    def test_get_value_from_dict(self):
        _dict = {
            "payload": {
                "compose": {
                    "date": "20180326",
                    "id": "Fedora-28-20180326.0",
                },
                "images": {
                    "AtomicHost": {
                        "aarch64": [
                            {
                                "arch": "aarch64",
                                "format": "qcow2",
                                "path": "AtomicHost/aarch64/images/Fedora-AtomicHost-28_Beta-1.1.aarch64.qcow2",
                            },
                            {
                                "arch": "aarch64",
                                "format": "raw.xz",
                                "path": "AtomicHost/aarch64/images/Fedora-AtomicHost-28_Beta-1.1.aarch64.raw.xz",
                            },
                        ]
                    }
                }
            }
        }

        valid_return = fedimg.utils.get_value_from_dict(_dict, 'payload', 'images', 'AtomicHost')
        invalid_return = fedimg.utils.get_value_from_dict(_dict, 'payload', 'images', 'Cloud')

        assert 'aarch64' in valid_return
        assert invalid_return == None

    @mock.patch('fedimg.utils.log.debug')
    def test_external_run_command(self, mock_log):
        mock_popen = TestFedimgUtils.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=(
            "2018-03-27 00:00:00 (93 KB/s) 'Fedora-Atomic-26-1.5.x86_64.raw.xz' (1234569/123456789)",
            ""
        ))
        mock_returncode = mock.PropertyMock(return_value=1)
        type(mock_popen).returncode = mock_returncode
        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)

        fedimg.utils.external_run_command('wget https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz -P /tmp/tmpABCDEF')

        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called_once_with()

    def test_get_item_from_regex(self):

        result = fedimg.utils.get_item_from_regex(
            'Task completed: import-vol-abc12345',
            '\s(import-vol-\w{8})'
        )

        assert result == 'import-vol-abc12345'

        negative_result = fedimg.utils.get_item_from_regex(
            'Task completed: import-vol-1234',
            '\s(import-vol-\w{8})'
        )

        assert negative_result == ''

    def test_get_file_name_image(self):

        result = fedimg.utils.get_file_name_image(
            'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz'
        )

        assert result == 'Fedora-Atomic-26-1.5.x86_64.raw.xz'

    @mock.patch('fedimg.utils.external_run_command')
    def test_get_source_from_image(self, mock_erc):
        mock_erc.return_value = (
            "2018-03-27 00:00:00 (93 KB/s) 'Fedora-Atomic-26-1.5.x86_64.raw.xz' (1234569/123456789)",
            "",
            0
        )
        fedimg.utils.get_source_from_image('https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz')

        mock_erc.assert_called_once_with([
            'wget',
            'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz',
            '-P',
            mock.ANY
        ])

    @mock.patch('fedimg.utils.external_run_command')
    def test_get_source_from_image_retcode_1(self, mock_erc):
        mock_erc.return_value = (
            "2018-03-27 00:00:00 (93 KB/s) 'Fedora-Atomic-26-1.5.x86_64.raw.xz' (1234569/123456789)",
            "",
            1
        )
        file_path = fedimg.utils.get_source_from_image('https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz')

        mock_erc.assert_called_once_with([
            'wget',
            'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz',
            '-P',
            mock.ANY
        ])
        assert file_path == ''

    def test_get_volume_type_from_image(self):
        mock_image = mock.Mock()
        mock_image.extra = {
            'block_device_mapping': [{
                'ebs': {
                    'volume_type': 'gp2'
                }
            }]
        }
        region = 'us-east-1'

        volume_type = fedimg.utils.get_volume_type_from_image(
                mock_image, region)

        assert volume_type == 'gp2'

    def test_get_virt_type_from_image_hvm(self):
        mock_image = mock.Mock()
        mock_image.extra = {
            'block_device_mapping': [{
                'device_name': '/dev/sda1'
            }]
        }

        virt_type = fedimg.utils.get_virt_type_from_image(mock_image)

        assert virt_type == 'hvm'

    def test_get_virt_type_from_image_paravirtual(self):
        mock_image = mock.Mock()
        mock_image.extra = {
            'block_device_mapping': [{
                'device_name': '/dev/sda'
            }]
        }

        virt_type = fedimg.utils.get_virt_type_from_image(mock_image)

        assert virt_type == 'paravirtual'

    def test_region_to_driver(self):
        driver_1 = fedimg.utils.region_to_driver('us-east-1')
        driver_2 = fedimg.utils.region_to_driver('eu-west-1')

        assert driver_1.func == driver_2.func

    @mock.patch('paramiko.SSHClient')
    def test_ssh_connection_works_true(self, mocksshclient):
        mocksshclient.connect.return_value = ''
        result = fedimg.utils.ssh_connection_works(
            'testuser',
            '127.0.0.1',
            '/path/to/key'
        )

        assert result == True

    @mock.patch('paramiko.SSHClient')
    def test_ssh_connection_works_false(self, mocksshclient):
        mockssh = mock.Mock()
        mocksshclient.return_value = mockssh
        mockssh.connect.side_effect = mock_ssh_exception
        result = fedimg.utils.ssh_connection_works(
            'testuser',
            '127.0.0.1',
            '/path/to/key'
        )

        assert result == False

    def test_get_image_name_from_image(self):
        image_name = fedimg.utils.get_image_name_from_image(
            'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz',
            'hvm',
            'us-east-1',
            '0',
            'gp2'
        )

        assert image_name == 'Fedora-Atomic-26-1.5.x86_64-hvm-us-east-1-gp2-0'

    def test_get_image_name_from_image_without_vol_type(self):
        image_name = fedimg.utils.get_image_name_from_image(
            image_url='https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz',
            virt_type='hvm',
            region='us-east-1',
            respin='0',
        )

        assert image_name == 'Fedora-Atomic-26-1.5.x86_64-hvm-us-east-1-0'

    def test_get_image_name_from_ami_name(self):
        image_name = fedimg.utils.get_image_name_from_ami_name(
            'Fedora-Cloud-Base-26-20180329.0.x86_64-paravirtual-us-east-1-gp2-0',
            'eu-west-1'
        )

        assert image_name == 'Fedora-Cloud-Base-26-20180329.0.x86_64-paravirtual-eu-west-1-gp2-0'

if __name__ == '__main__':
    unittest.main()
