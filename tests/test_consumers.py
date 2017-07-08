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
import mock
import requests
import unittest

import vcr

import fedimg.consumers

cassette_dir = os.path.join(os.path.dirname(__file__), 'vcr-request-data')


class TestFedimgConsumer(unittest.TestCase):
    """ Comment goes here """

    @classmethod
    def setUpClass(cls):
        import fedmsg.config
        import fedmsg.meta

        config = fedmsg.config.load_config([], None)
        fedmsg.meta.make_processors(**config)
        cls.fedmsg_config = config

    def setUp(self):
        vcr_filename = os.path.join(cassette_dir, self.id())
        self.vcr = vcr.use_cassette(vcr_filename, record_mode='new_episodes')
        self.vcr.__enter__()

        class FakeHub(object):
            config = self.fedmsg_config

            def subscribe(*args, **kwargs):
                pass

        fedimg.consumers.FedimgConsumer._initialized = True  # a lie
        self.consumer = fedimg.consumers.FedimgConsumer(FakeHub())

    def tearDown(self):
        pass

    @mock.patch('fedimg.uploader.upload')
    def test_send_to_uploader(self, upload):
        msg = {
            'topic': 'org.fedoraproject.prod.pungi.compose.status.change',
            'body': {
                'msg_id': 1,
                'msg': {
                    'status': 'FINISHED_INCOMPLETE',
                    'location': 'http://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-20170708.n.0/compose', 
                    'compose_id': 'Fedora-Rawhide-20170708.n.0'
                }
            }
        }

        self.consumer.consume(msg)
        url = 'http://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-20170708.n.0/compose/CloudImages/x86_64/images/Fedora-Cloud-Base-Rawhide-20170708.n.0.x86_64.raw.xz'
        upload.assert_called_with(mock.ANY, [url], 'Fedora-Rawhide-20170708.n.0')

if __name__ == '__main__':
    unittest.main()
