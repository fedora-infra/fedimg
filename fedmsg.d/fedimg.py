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
#

import socket
hostname = socket.gethostname()

NUM_BASE_THREADS = 4
NUM_ATOMIC_THREADS = 2
NUM_PORTS = 2 * ((NUM_BASE_THREADS + NUM_ATOMIC_THREADS) + 1)

config = {
    'fedimgconsumer.dev.enabled': True,
    'fedimgconsumer.prod.enabled': False,
    'fedimgconsumer.stg.enabled': False,
    'endpoints': {
        "fedimg.%s" % hostname: [
            "tcp://127.0.0.1:60%0.2i" % (i)
            for i in range(NUM_PORTS)
        ],
    },
}
