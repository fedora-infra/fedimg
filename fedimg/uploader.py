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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#

import logging
log = logging.getLogger("fedmsg")

from fedimg.services.ec2 import EC2Service
from fedimg.util import virt_types_from_url


def upload(pool, urls, compose_meta):
    """ Takes a list (urls) of one or more .raw.xz image files and
    sends them off to cloud services for registration. The upload
    jobs threadpool must be passed as `pool`."""

    log.info('Starting upload process')

    services = []

    for url in urls:
        # EC2 upload
        log.info("  Preparing to upload %r" % url)
        for vt in virt_types_from_url(url):
            services.append(EC2Service(url, virt_type=vt,
                                       vol_type='standard'))
            services.append(EC2Service(url, virt_type=vt,
                                       vol_type='gp2'))

    results = pool.map(lambda s: s.upload(compose_meta), services)
