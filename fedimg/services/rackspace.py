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


class RackspaceServiceException(Exception):
    """ Custom exception for RackspaceService. """
    pass


class RackspaceService(object):
    """ A class for interacting with a Rackspace connection. """

    def __init__(self):

        self.regions = ['dfw', 'ord', 'iad', 'lon', 'syd', 'hkg']

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an image
        in each Rackspace region. """

        cls = get_driver(Provider.RACKSPACE)
        driver = cls(fedimg.RACKSPACE_USER, fedimg.RACKSPACE_API_KEY,
                     region=self.regions[0])

        # create image from official Fedora image on Rackspace

        # emit a fedmsg, etc
