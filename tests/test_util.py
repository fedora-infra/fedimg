# This file is part of fedimg.
# Copyright (C) 2014 Red Hat, Inc.
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
#

import mock
import unittest

import fedimg
import fedimg.util


class TestUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_file_arch(self):
        filename = 'fedora-cloud-base-20140915-21.i386.raw.xz'
        arch = fedimg.util.get_file_arch(filename)
        self.assertEquals(arch, 'i386')
        filename = 'fedora-cloud-base-20140915-21.x86_64.raw.xz'
        arch = fedimg.util.get_file_arch(filename)
        self.assertEquals(arch, 'x86_64')

    def test_get_rawxz_url(self):
        task_result = {'arch': 'i386',
                       'files': ['fedora-cloud-base-a89507d.ks',
                                 'koji-f21-build-7577982-base.ks',
                                 'tdl-i386.xml', 'qemu-img-qcow2-i386.log',
                                 'xz-cp-raw-xz-i386.log', 'xz-raw-xz-i386.log',
                                 'oz-i386.log', 'libvirt-qcow2-i386.xml',
                                 'fedora-cloud-base-20140915-21.i386.qcow2',
                                 'libvirt-raw-xz-i386.xml',
                                 'fedora-cloud-base-20140915-21.i386.raw.xz'],
                       'name': 'fedora-cloud-base',
                       'release': '21',
                       'rpmlist': [],
                       'task_id': 7577982,
                       'version': '20140915'}

        # extension to base URL to exact file directory
        filename = 'fedora-cloud-base-20140915-21.i386.raw.xz'
        koji_url_extension = "/7982/7577982"
        full_task_url = fedimg.BASE_KOJI_TASK_URL + koji_url_extension
        full_file_url = full_task_url + '/' + filename

        url = fedimg.util.get_rawxz_url(task_result)
        self.assertEquals(url, full_file_url)

    def test_get_rawxz_url_empty(self):
        task_result = {'arch': 'i386',
                       'files': ['fedora-cloud-base-a89507d.ks',
                                 'koji-f21-build-7577982-base.ks',
                                 'tdl-i386.xml', 'qemu-img-qcow2-i386.log',
                                 'xz-cp-raw-xz-i386.log', 'xz-raw-xz-i386.log',
                                 'oz-i386.log', 'libvirt-qcow2-i386.xml',
                                 'fedora-cloud-base-20140915-21.i386.qcow2',
                                 'libvirt-raw-xz-i386.xml'],
                       'name': 'fedora-cloud-base',
                       'release': '21',
                       'rpmlist': [],
                       'task_id': 7577982,
                       'version': '20140915'}

        # extension to base URL to exact file directory
        filename = 'fedora-cloud-base-20140915-21.i386.raw.xz'
        koji_url_extension = "/7982/7577982"
        full_task_url = fedimg.BASE_KOJI_TASK_URL + koji_url_extension
        full_file_url = full_task_url + '/' + filename

        url = fedimg.util.get_rawxz_url(task_result)
        self.assertEquals(url, None)

    def test_virt_types(self):
        url = 'https://somepage.org/fedora-cloud-base-20140915-21.x86_64.raw.xz'
        vtypes = fedimg.util.virt_types_from_url(url)
        self.assertEqual(vtypes, ['hvm', 'paravirtual'])

        url = 'https://somepage.org/fedora-cloud-atomic-20140915-21.x86_64.raw.xz'
        vtypes = fedimg.util.virt_types_from_url(url)
        self.assertEqual(vtypes, ['hvm'])


if __name__ == '__main__':
    unittest.main()
