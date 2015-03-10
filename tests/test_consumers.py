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

import mock
import requests
import unittest

import fedmsg

import fedimg.consumers


class TestKojiConsumer(unittest.TestCase):
    """ Fedimg should pick up on completed createImage Koji tasks and kick off
    the upload process if they produce an image we want to upload. """

    @classmethod
    def setUpClass(cls):
        import fedmsg.config
        import fedmsg.meta

        config = fedmsg.config.load_config([], None)
        fedmsg.meta.make_processors(**config)
        cls.fedmsg_config = config

    def setUp(self):
        class FakeHub(object):
            config = self.fedmsg_config

            def subscribe(*args, **kwargs):
                pass

        fedimg.consumers.KojiConsumer._initialized = True  # a lie
        self.consumer = fedimg.consumers.KojiConsumer(FakeHub())

    def tearDown(self):
        pass

    @mock.patch('fedimg.uploader.upload')
    def test_send_to_uploader(self, upload):
        # I just pull the msg from the web for now.
        # I will later put it in a text file or something I guess?
        # Below is an image task with two createImage children.
        koji_msg_id = '2014-e9065d79-8975-4b3d-897e-fcc807ba95dd'
        datagrepper_url = 'https://apps.fedoraproject.org/datagrepper/id?id={0}'.format(koji_msg_id)
        resp = requests.get(datagrepper_url)

        # Need to wrap the message in a body dict to emulate how an actual
        # consumed fedmsg would come through.
        msg = {'topic': 'org.fedoraproject.prod.buildsys.task.state.change',
                'body': {'msg': resp.json()['msg'],
                        'msg_id': 1}}

        self.consumer.consume(msg)
        # the list seems to always be newest task first
        url1 = ('https://kojipkgs.fedoraproject.org//work/tasks/7981/7577981/'
                'fedora-cloud-base-20140915-21.x86_64.raw.xz')
        upload.assert_called_with([url1])

if __name__ == '__main__':
    unittest.main()
