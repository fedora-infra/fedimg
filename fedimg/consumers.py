#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg.consumers
import fedmsg.encoding

import fedimg.uploader


class KojiConsumer(fedmsg.consumers.FedmsgConsumer):
    # To our knowledge, all *image* builds appear under this
    # exact topic, along with scratch builds.
    topic = 'org.fedoraproject.prod.buildsys.task.state.change'
    config_key = 'kojiconsumer'

    def __init__(self, *args, **kwargs):
        super(KojiConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        """Here we put what we'd like to do when we receive the message."""

        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]

        # If the build method is "image", we check to see if the child
        # task's method is "createImage".
        if msg_info["method"] == "image":
            if isinstance(msg_info["children"], list):
                for child in msg_info["children"]:
                    if child["method"] == "createImage":
                        # We only care about the image if the build
                        # completed successfully (with state code 2).
                        if child["state"] == 2:
                            builds.append(child["id"])
        if len(builds) > 0:
            fedimg.uploader.upload(builds)
