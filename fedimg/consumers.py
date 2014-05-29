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
        build_method = msg["msg"]["info"]["method"]["image"]
        # If the build method is "image", we check to see if the child
        # task's method is "createImage".
        if build_method = "image":
            # TODO: Continue to the child task and check its method
            # as per the above comment.
            pass
