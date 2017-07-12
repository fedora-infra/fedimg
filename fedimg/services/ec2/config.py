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


import toml

# Read in config file
with open("/etc/fedimg/fedimg-conf.toml") as conffile:
    config = toml.loads(conffile.read())

UTIL_USER = config.get('aws', 'util_username')
TEST_USER = config.get('aws', 'test_username')
ACCESS_ID = config.get('aws', 'access_id')
SECRET_KEY = config.get('aws', 'secret_key')
VOLUME_SIZE = config.get('aws', 'volume_size')
VOLUME_TYPES = config.get('aws', 'volume_types')
VOLUME_VIA_S3 = config.get('aws', 'volume_via_s3')
IAM_PROFILE = config.get('aws', 'iam_profile')
REGIONS = config.get('aws', 'regions')
