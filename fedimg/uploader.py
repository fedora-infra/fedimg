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

import multiprocessing.pool

from fedimg.services.ec2 import EC2Service
from fedimg.util import virt_types_from_url


def upload(urls):
    """ Takes a list of one or more .raw.xz image files and
    sends them off to cloud services for registration. """

    log.info('Starting upload process')

    # We're not going to have more that 2 services at this point
    pool = multiprocessing.pool.ThreadPool(processes=4)

    services = []

    # TODO: Thread this process
    for url in urls:
        # EC2 upload
        for vt in virt_types_from_url(url):
            services.append(EC2Service(url, virt_type=vt,
                                       vol_type='standard'))
            services.append(EC2Service(url, virt_type=vt,
                                       vol_type='gp2'))

    results = pool.map(lambda s: s.upload(), services)

    log.info('Upload process finished')
