# This file is part of fedimg.
# Copyright (C) 2015 Red Hat, Inc.
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
# Authors:  Ralph Bean <rbean@redhat.com>
#
""" hacks.

Primarily, this is used to monkeypatch libcloud at runtime to give it support
for the ec2 eu-central-1 region which it amazingly doesn't have support for out
of the box.  We have to define a driver for it and then inject our driver into
its registry of providers.

This needs to happen early on in the fedimg process... before
fedimg.util.region_to_provider is invoked.

"""

import libcloud.compute.types
import libcloud.compute.providers
import libcloud.compute.drivers.ec2

import logging
log = logging.getLogger('fedmsg')


class EC2EUCentralNodeDriver(libcloud.compute.drivers.ec2.EC2NodeDriver):
    """
    Driver class for EC2 in the EU Central Frankfurt region.
    """
    name = 'Amazon EC2 (eu-central-1)'
    _region = 'eu-central-1'


def monkeypatch_libcloud():
    """ Call this to inject a eu-central-1 driver into libcloud's registry. """
    key = 'ec2_eu_central'
    if key in libcloud.compute.providers.DRIVERS:
        log.info("libcloud now supports %r.  Not patching." % key)
    else:
        log.warn("monkey patching libcloud with support for %r" % key)
        path = ('fedimg.haxx', 'EC2EUCentralNodeDriver')
        libcloud.compute.types.Provider.EC2_EU_CENTRAL = key
        libcloud.compute.providers.DRIVERS[key] = path


if __name__ == '__main__':
    logging.basicConfig()
    monkeypatch_libcloud()

    # A test...
    import fedimg.util
    provider = fedimg.util.region_to_provider('eu-central-1')
    driver = libcloud.compute.providers.get_driver(provider)
    print driver  # It works!
