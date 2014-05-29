#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg.consumers


class KojiConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.buildsys.*'
    config_key = 'kojiconsumer'

    def __init__(self, *args, **kwargs):
        super(KojiConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        """Here we put what we'd like to do when we receive the message."""
        pass
