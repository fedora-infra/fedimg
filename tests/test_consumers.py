# This file is part of fedimg.
# Copyright (C) 2018 Red Hat, Inc.
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
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
#

import os
import mock
import unittest

import vcr

import fedimg.consumers

import utils


cassette_dir = os.path.join(os.path.dirname(__file__), 'vcr-request-data')


class TestFedimgConsumer(unittest.TestCase):

    def setUp(self):
        hub = utils.MockHub()
        self.consumer = fedimg.consumers.FedimgConsumer(hub)

        vcr_filename = os.path.join(cassette_dir, self.id())
        self.vcr = vcr.use_cassette(vcr_filename, record_mode='new_episodes')
        self.vcr.__enter__()

    def tearDown(self):
        self.vcr.__exit__()

    @mock.patch('fedimg.consumers._log.debug')
    @mock.patch('fedimg.uploader.upload')
    def test_invalid_status(self, mock_upload, mock_log):
        msg = {
            "topic": "org.fedoraproject.prod.pungi.compose.status.change",
            "body":  {
                "username": "root",
                "i": 1,
                "timestamp": 1521703054.0,
                "msg_id": "2018-6de5ec39-0e28-46aa-a359-99142682fdd9",
                "topic": "org.fedoraproject.prod.pungi.compose.status.change",
                "msg": {
                    "status": "STARTED",
                    "release_type": "ga",
                    "compose_label": None,
                    "compose_respin": 0,
                    "compose_date": "20180321",
                    "release_version": "28",
                    "location": "http://kojipkgs.fedoraproject.org/compose/branched/Fedora-28-20180321.n.0/compose",
                    "compose_type": "nightly",
                    "release_is_layered": False,
                    "release_name": "Fedora",
                    "release_short": "Fedora",
                    "compose_id": "Fedora-28-20180321.n.0"
                }
            }
        }
        self.consumer.consume(msg)
        mock_log.assert_called_with('STARTED is not valid status')

    @mock.patch('fedimg.consumers._log.debug')
    @mock.patch('fedimg.uploader.upload')
    def test_incompatible_images(self, mock_upload, mock_log):
        msg = {
            "topic": "org.fedoraproject.prod.pungi.compose.status.change",
            "body":  {
                "username": "root",
                "i": 1,
                "timestamp": 1521648937.0,
                "msg_id": "2018-31162ce8-69ec-417e-bc7f-01653f4dcedf",
                "topic": "org.fedoraproject.prod.pungi.compose.status.change",
                "msg": {
                    "status": "FINISHED_INCOMPLETE",
                    "release_type": "ga",
                    "compose_label": None,
                    "compose_respin": 0,
                    "compose_date": "20180426",
                    "release_version": "Rawhide",
                    "location": "http://kojipkgs.fedoraproject.org/compose/rawhide/Fedora-Rawhide-20180426.n.0/compose",
                    "compose_type": "nightly",
                    "release_is_layered": False,
                    "release_name": "Fedora",
                    "release_short": "Fedora",
                    "compose_id": "Fedora-Rawhide-20180426.n.0"
                }
            }
        }
        self.consumer.consume(msg)
        mock_log.assert_called_with('No compatible image found to process')

    @mock.patch('fedimg.uploader.upload')
    def test_success_upload(self, upload):
        msg = {
            "topic": "org.fedoraproject.prod.pungi.compose.status.change",
            "body":  {
                "username": "root",
                "i": 1,
                "timestamp": 1521271546.0,
                "msg_id": "2018-8c8c2c46-e5f8-4fe3-8f8b-80dd18b21947",
                "topic": "org.fedoraproject.prod.pungi.compose.status.change",
                "msg": {
                    "status": "FINISHED",
                    "release_type": "ga",
                    "compose_label": "RC-20180425.0",
                    "compose_respin": 0,
                    "compose_date": "20180425",
                    "release_version": "28",
                    "location": "https://kojipkgs.fedoraproject.org/compose/28/latest-Fedora-28/compose",
                    "compose_type": "production",
                    "release_is_layered": False,
                    "release_name": "Fedora-Cloud",
                    "release_short": "Fedora-Cloud",
                    "compose_id": "Fedora-28-20180425.0"
                }
            }
        }

        self.consumer.consume(msg)
        url = 'https://kojipkgs.fedoraproject.org/compose/28/latest-Fedora-28/compose/Cloud/x86_64/images/Fedora-Cloud-Base-28-1.1.x86_64.raw.xz'
        url1 = 'https://kojipkgs.fedoraproject.org/compose/28/latest-Fedora-28/compose/AtomicHost/x86_64/images/Fedora-AtomicHost-28-1.1.x86_64.raw.xz'
        upload.assert_called_with(
            pool=mock.ANY,
            urls=[url, url1],
            compose_id='Fedora-28-20180425.0',
            push_notifications=True
        )
