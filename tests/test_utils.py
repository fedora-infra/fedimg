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

import fedimg
import fedimg.utils


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

if __name__ == '__main__':
    unittest.main()
