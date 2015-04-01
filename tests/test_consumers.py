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
        resp_json = resp.json()
        resp_msg = resp_json['msg']

        # Need to wrap the message in a body dict to emulate how an actual
        # consumed fedmsg would come through.
        msg = {'topic': 'org.fedoraproject.prod.buildsys.task.state.change',
                'body': {'msg': resp_msg,
                        'msg_id': 1}}

        self.consumer.consume(msg)
        # the list seems to always be newest task first
        url1 = ('https://kojipkgs.fedoraproject.org//work/tasks/7981/7577981/'
                'fedora-cloud-base-20140915-21.x86_64.raw.xz')
        upload.assert_called_with(mock.ANY, [url1])

    #@mock.patch('fedimg.uploader.upload')
    def test_get_upload_urls(self):
        upload_files = self.consumer._get_upload_urls([9203308])
        url = 'https://kojipkgs.fedoraproject.org//work/tasks/3308/9203308/Fedora-Cloud-Base-22_Beta_TC1-20150310.x86_64.raw.xz'
        self.assertEquals(len(upload_files), 1)
        self.assertEquals(upload_files[0], url)
    
    def test_get_upload_urls_atomic(self):
        upload_files = self.consumer._get_upload_urls([9203313])
        url = 'https://kojipkgs.fedoraproject.org//work/tasks/3313/9203313/Fedora-Cloud-Atomic-22_Beta_TC1-20150310.x86_64.raw.xz'
        self.assertEquals(len(upload_files), 1)
        self.assertEquals(upload_files[0], url)
        
    def test_get_upload_urls_i386(self):
        upload_files = self.consumer._get_upload_urls([9203309])
        # we don't upload 32 bit images at this time
        self.assertEquals(len(upload_files), 0)
    
    def test_get_upload_urls_vagrant(self):
        upload_files = self.consumer._get_upload_urls([9203314])
        # we don't upload vagrant images at this time
        self.assertEquals(len(upload_files), 0)

if __name__ == '__main__':
    unittest.main()
