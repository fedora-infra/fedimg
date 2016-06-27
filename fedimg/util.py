# This file is part of fedimg.
# Copyright (C) 2014-2015 Red Hat, Inc.
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
#           Ralph Bean <rbean@redhat.com>
#

"""
Utility functions for fedimg.
"""

import functools
import socket
import subprocess

import paramiko
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import fedimg


def get_file_arch(file_name):
    """ Takes a file name (probably of a .raw.xz image file) and returns
    the suspected architecture of the contained image. If it doesn't look
    like a 32-bit or 64-bit image, None is returned. """
    if file_name.find('i386') != -1:
        return 'i386'
    elif file_name.find('x86_64') != -1:
        return 'x86_64'
    else:
        return None


def get_rawxz_urls(location, images):
    """ Iterates through all the images metadata and returns the url of .raw.xz
    files.
    """
    rawxz_list = [f['path'] for f in images if f['path'].endswith('.raw.xz')]
    if not rawxz_list:
        return []

    return map((lambda path: '{}/{}'.format(location, path)), rawxz_list)


def virt_types_from_url(url):
    """ Takes a URL to a .raw.xz image file) and returns the suspected
        virtualization type that the image file should be registered as. """
    file_name = url.split('/')[-1].lower()
    if file_name.find('atomic') != -1:
        # hvm is required for atomic images
        return ['hvm']
    else:
        # otherwise, build the AMIs with both virtualization types
        return ['hvm', 'paravirtual']


def region_to_driver(region):
    """ Takes a region name (ex. 'eu-west-1') and returns
    the appropriate libcloud provider value. """
    cls = get_driver(Provider.EC2)
    return functools.partial(cls, region=region)


def ssh_connection_works(username, ip, keypath):
    """ Returns True if an SSH connection can me made to `username`@`ip`. """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    works = False
    try:
        ssh.connect(ip, username=username,
                    key_filename=keypath)
        works = True
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException, socket.error) as e:
        pass
    ssh.close()
    return works


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct
