#!/bin/env python
# -*- coding: utf8 -*-

import koji


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """
    if isinstance(builds, list):
        # Create a Koji connection to the Fedora Koji instance
        koji_server = "https://koji.fedoraproject.org/kojihub"
        koji_session = koji.ClientSession(koji_server)

        upload_files = list()

        def get_qcow2_files(task_output):
            # I think there might only ever be one qcow2 file per task,
            # but doing it this way plays it safe.
            return [f for f in task_output if ".qcow2" in f]

        if len(builds) == 1:
            task_output = koji_session.listTaskOutput(builds[0])
            upload_files.extend(get_qcow2_files(task_output))
        elif len(builds) >= 2:
            # This is the edge case -- in fact, I don't even know if it
            # can happen, ever. Therefore, TODO: can this code ever be called?
            task_outputs = list()  # will be a list of task output lists
            koji.multicall = True
            for build in builds:
                koji_session.listTaskOutput(build)
            results = koji.multiCall()
            for result in results:
                upload_files.extend(get_qcow2_files(result))
            koji.multicall = False  # TODO: Is this needed?

    # ACTUAL UPLOAD CODE WILL GO HERE

    else:
        # TODO: Not sure if this is the proper way to handle this.
        raise Exception("Build upload function must take a list.")
        return  # TODO: Does this need to go here?
