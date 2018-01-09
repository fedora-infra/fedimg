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

# Fedimg Consumer configurations
PROCESS_COUNT = config['general']['process_count']
STATUS_FILTER = ('FINISHED_INCOMPLETE', 'FINISHED')

ACTIVE_SERVICES = config['general']['active_services']
CLEAN_UP_ON_FAILURE = config['general']['clean_up_on_failure']
DELETE_IMAGES_ON_FAILURE = config['general']['delete_images_on_failure']

AWS_UTIL_USER = config.get('aws', {}).get('util_username', {})
AWS_TEST_USER = config.get('aws', {}).get('test_username', {})
AWS_ACCESS_ID = config.get('aws', {}).get('access_id')
AWS_SECRET_KEY = config.get('aws', {}).get('secret_key')
AWS_VOLUME_SIZE = config.get('aws', {}).get('volume_size')
AWS_VOLUME_TYPES = config.get('aws', {}).get('volume_types')
AWS_VOLUME_VIA_S3 = config.get('aws', {}).get('volume_via_s3')
AWS_IAM_PROFILE = config.get('aws', {}).get('iam_profile')
AWS_REGIONS = config.get('aws', {}).get('regions', {})
AWS_ROOT_VOLUME_SIZE = config.get('aws', {}).get('root_volume_size', {})
AWS_BASE_REGION = config.get('aws', {}).get('base_region', {})
AWS_DELETE_RESOURCES = config.get('aws', {}).get('delete_resources', True)
