#!/bin/env python
# -*- coding: utf8 -*-

import koji


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """
    # Error out if the "builds" argument passed to upload() is not a list.
    if not isinstance(builds, list):
        # TODO: Not sure if this is the proper way to handle this.
        raise Exception("Build upload function must take a list.")
        return  # TODO: Does this need to go here?

    # Create a Koji connection to the Fedora Koji instance
    koji_server = "https://koji.fedoraproject.org/kojihub"
    koji_session = koji.ClientSession(koji_server)

    # The two slashes ("//") in the following URL are NOT a mistake.
    base_koji_task_url = "https://kojipkgs.fedoraproject.org//work/tasks"

    upload_files = list()  # list of full URLs of files

    def get_qcow2_files(task_result):
        # I think there might only ever be one qcow2 file per task,
        # but doing it this way plays it safe.
        file_names = [f for f in task_result['files'] if ".qcow2" in f]
        task_id = task_result['task_id']

        # extension to base URL to exact file directory
        koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
        full_file_location = base_koji_task_url + koji_url_extension

        file_urls = list()  # full URLs of qcow2 files
        for f in file_names:
            file_urls.append(full_file_location + "/{}".format(f))

        return file_urls

    if len(builds) == 1:
        task_result = koji_session.getTaskResult(builds[0])
        upload_files.extend(get_qcow2_files(task_result))
    elif len(builds) >= 2:
        # This is the edge case -- in fact, I don't even know if it
        # can happen, ever. Therefore, TODO: can this code ever be called?
        koji.multicall = True
        for build in builds:
            koji_session.listTaskOutput(build)
        results = koji.multiCall()
        for result in results:
            upload_files.extend(get_qcow2_files(result))
        koji.multicall = False  # TODO: Is this needed?

    for f in upload_files:
        print "Would upload file at {}\n".format(f)
