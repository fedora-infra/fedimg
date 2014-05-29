#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg.consumers
import fedmsg.encoding


class KojiConsumer(fedmsg.consumers.FedmsgConsumer):
    # To our knowledge, all *image* builds appear under this
    # exact topic, along with scratch builds.
    topic = 'org.fedoraproject.prod.buildsys.task.state.change'
    config_key = 'kojiconsumer'

    def __init__(self, *args, **kwargs):
        super(KojiConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        """Here we put what we'd like to do when we receive the message."""
        # Convert JSON string representation to a Python data structure
        msg = fedmsg.encoding.loads(msg)
