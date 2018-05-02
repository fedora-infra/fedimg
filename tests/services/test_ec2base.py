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

from fedimg.services.ec2.ec2base import EC2Base
from libcloud.compute.drivers.ec2 import EC2NodeDriver


class TestEC2Base(unittest.TestCase):

    def setUp(self):
        self.ec2base_obj = EC2Base()
        setattr(self.ec2base_obj, 'access_key', 'ABCDEFGHIJKLMNO123456789')
        setattr(self.ec2base_obj, 'secret_key', 'THISISASECRETKEYWITH0987')
        setattr(self.ec2base_obj, 'region', 'us-east-1')

    def test_connect(self):
        driver = self.ec2base_obj._connect()

        self.assertTrue(isinstance(driver, EC2NodeDriver))

    def test_set_region(self):
        self.ec2base_obj.set_region('eu-east-1')
        self.assertEqual(self.ec2base_obj.region, 'eu-east-1')

