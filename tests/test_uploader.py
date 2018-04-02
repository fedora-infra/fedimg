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
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

import mock
import multiprocessing.pool
import unittest

import fedimg.uploader


class TestUploader(unittest.TestCase):

    @mock.patch('fedimg.uploader.ec2main', return_value=[])
    @mock.patch('fedimg.uploader.ec2copy')
    @mock.patch('fedimg.uploader.ACTIVE_SERVICES', return_value=['hp'])
    def test_inactive_aws(self, active_services, ec2copy, ec2main):

        thread_pool = multiprocessing.pool.ThreadPool(processes=1)

        fedimg.uploader.upload(
            thread_pool,
            ['http://kojipkgs.fedoraproject.org/compose/Fedora-Cloud-27-20180317.0/compose/CloudImages/x86_64/images/Fedora-Cloud-Base-27-20180317.0.x86_64.raw.xz'],
            compose_id='Fedora-Cloud-27-20180317.0'
        )

        assert ec2main.called == False
        assert ec2copy.called == False

    @mock.patch('fedimg.uploader.ec2main', return_value=[])
    @mock.patch('fedimg.uploader.ec2copy')
    def test_active_aws_no_images(self, ec2copy, ec2main):
        thread_pool = multiprocessing.pool.ThreadPool(processes=1)

        fedimg.uploader.upload(
            thread_pool,
            ['http://kojipkgs.fedoraproject.org/compose/Fedora-Cloud-27-20180317.0/compose/CloudImages/x86_64/images/Fedora-Cloud-Base-27-20180317.0.x86_64.raw.xz'],
            compose_id='Fedora-Cloud-27-20180317.0'
        )

        assert ec2main.called == True
        assert ec2copy.called == False

    @mock.patch('fedimg.uploader.ec2main')
    @mock.patch('fedimg.uploader.ec2copy')
    def test_active_aws_with_images(self, ec2copy, ec2main):
        thread_pool = multiprocessing.pool.ThreadPool(processes=1)
        ec2main.return_value = [{
            'image_id': 'i-abc1234',
            'is_image_public': True,
            'snapshot_id': 'snap-abc1234',
            'is_snapshot_public': True,
            'regions': 'us-east-1'
        }]

        fedimg.uploader.upload(
            thread_pool,
            ['http://kojipkgs.fedoraproject.org/compose/Fedora-Cloud-27-20180317.0/compose/CloudImages/x86_64/images/Fedora-Cloud-Base-27-20180317.0.x86_64.raw.xz'],
            compose_id='Fedora-Cloud-27-20180317.0'
        )

        assert ec2main.called == True
        assert ec2copy.called == True

if __name__ == '__main__':
    unittest.main()
