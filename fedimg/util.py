#!/bin/env python
# -*- coding: utf8 -*-
"""
Utility functions for fedimg.
"""

import fedimg


def compress(file_path):
    """ Compress a downloaded image file into a tar.xz file. """
    xz_file_path = file_path + ".tar.xz"
    subprocess.call(['tar', '-cfJ', xz_file_path, file_path])
    # TODO: Remove the original, uncompressed image file?
    # That is, assuming it's not needed for upload to cloud services.


def get_qcow2_files(task_result):
    """ Returns a list of URLs to qcow2 files produced by the Koji
    task ID represented by the task_result argument. """
    # I think there might only ever be one qcow2 file per task,
    # but doing it this way plays it safe.
    file_names = [f for f in task_result['files'] if ".qcow2" in f]
    task_id = task_result['task_id']

    # extension to base URL to exact file directory
    koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
    full_file_location = fedimg.BASE_KOJI_TASK_URL + koji_url_extension

    file_urls = list()  # full URLs of qcow2 files
    for f in file_names:
        file_urls.append(full_file_location + "/{}".format(f))

    return file_urls


def qcow2_to_raw(file_path):
    """ Takes the file path of a qcow2 image file and creates a .RAW conversion
    of the image. """
    if file_path.split('.')[-1] != 'qcow2':
        # TODO: logging here
        raise Exception("{0} is not a .qcow2 file.".format(file_path))

    # this is where I'll convert the image, once I decide on the proper tool
