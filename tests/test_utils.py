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

import fedimg
import fedimg.utils


class TestUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
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

        urls = fedimg.utils.get_rawxz_urls('https://somepage.org', images)
        atomic_url = 'https://somepage.org/CloudImages/x86_64/images/Fedora-Atomic-26-1.5.x86_64.raw.xz'
        cloud_base_url = 'https://somepage.org/CloudImages/x86_64/images/Fedora-Cloud-Base-26-1.5.x86_64.raw.xz'

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

    def test_virt_types(self):
        url = 'https://somepage.org/Fedora-Cloud-Base-26-1.5.x86_64.raw.xz'
        vtypes = fedimg.utils.get_virt_types_from_url(url)
        assert vtypes == ['hvm', 'paravirtual']

        url = 'https://somepage.org/Fedora-Atomic-26-1.5.x86_64.raw.xz'
        vtypes = fedimg.utils.get_virt_types_from_url(url)
        assert vtypes == ['hvm']


if __name__ == '__main__':
    unittest.main()
