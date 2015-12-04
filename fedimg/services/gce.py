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

import os
import subprocess

from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider, DeploymentException

import fedimg


class GCEServiceException(Exception):
    """ Custom exception for GCE. """
    pass


class GCEService(object):
    """ A class for interacting with a GCE connection. """

    def __init__(self):
        self.datacenters = ['us-central1-a']

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an image
        in each Rackspace region. """

        cls = get_driver(Provider.GCE)
        driver = cls(fedimg.GCE_EMAIL, fedimg.GCE_KEYPATH,
                     project=fedimg.GCE_PROJECT_ID,
                     datacenter=self.datacenters[0])

        # create image from official Fedora image on GCE

        # emit a fedmsg, etc
