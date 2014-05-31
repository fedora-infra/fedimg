#!/bin/env python
# -*- coding: utf8 -*-

import koji

from pprint import pprint


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """
    if isinstance(builds, list):
        # Create a Koji connection to the Fedora Koji instance
        koji_server = "https://koji.fedoraproject.org/kojihub"
        koji_session = koji.ClientSession(koji_server)
        if len(builds) == 1:
            print "\nRESULTS FOR listTaskOutput():\n"
            pprint(koji_session.listTaskOutput(builds[0]))
            print "\nRESULTS FOR getTaskResult():\n"
            pprint(koji_session.getTaskResult(builds[0]))
        elif len(builds) >= 2:
            #koji.multicall = True
            for build in builds:
                print "\nPLACEHOLDER FOR MULTICALL BUILD SITUATION\n"
            #results = koji.multiCall()
            #koji.multicall = False  # TODO: Is this needed?
    else:
        # TODO: Not sure if this is the proper way to handle this.
        raise Exception("Build upload function must take a list.")
        return  # TODO: Does this need to go here?
