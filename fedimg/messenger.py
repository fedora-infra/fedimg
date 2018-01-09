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

import fedmsg

"""
The latest Fedmsg meta code for Fedimg fedmsgs (what a mouthful!):
https://github.com/fedora-infra/fedmsg_meta_fedora_infrastructure/blob/develop/fedmsg_meta_fedora_infrastructure/fedimg.py
"""


def notify(topic, msg):
    """ Takes a message topic, image name, an upload destination (ex.
    "EC2-eu-west-1"), and a status (ex. "failed"). Can also take an optional
    dictionary of addiitonal bits of information, such as an AMI ID for an
    image registered to AWS EC2. Emits a fedmsg appropriate
    for each image task (an upload or a test). """

    fedmsg.publish(topic=topic, modname='fedimg', msg=msg)
