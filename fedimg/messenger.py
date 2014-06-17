#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg


def message(image_name, dest, status):
    """ Takes an upload destination (ex. "EC2-east") and a status (ex.
    "failed"). Emits a fedmsg appropriate for each image upload task. """

    topic = 'image.upload'

    fedmsg.publish(topic=topic, modname='fedimg', msg={
        'image_name': image_name,
        'destination': dest,
        'status': status,
    })
