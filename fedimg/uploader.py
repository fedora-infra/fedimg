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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

import logging
log = logging.getLogger("fedmsg")

from fedimg.config import ACTIVE_SERVICES
from fedimg.services.ec2.ec2initiate import main as ec2main

def upload(pool, urls, *args, **kwargs):
    """ Takes a list (urls) of one or more .raw.xz image files and
    sends them off to cloud services for registration. The upload
    jobs threadpool must be passed as `pool`."""

    active_services = ACTIVE_SERVICES

    if 'aws' in active_services:
        ec2main(urls)
