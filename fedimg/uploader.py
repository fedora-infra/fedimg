#!/bin/env python
# -*- coding: utf8 -*-

import koji


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """
    if isinstance(builds, list):
        for build in builds:
            pass
    else:
        # TODO: Not sure if this is the proper way to handle this.
        raise Exception("Build upload function must take a list.")
        return  # TODO: Does this need to go here?
