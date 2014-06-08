#!/bin/env python
# -*- coding: utf8 -*-
"""
Utility functions for fedimg.
"""

import subprocess

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
    """ Takes the file path of a qcow2 image file and creates a .raw conversion
    of the image. Returns the file path to the new raw image. qcow2 files are
    smaller than raw images, so this function saves us time by downloading only
    one, smaller file and then converting it for services requiring raw image
    files. """
    if file_path.endswith('.qcow2'):
        raw_file_path = file_path[:5] + '.raw'
        try:
            # TODO: Wait for completion on this conversion?
            subprocess.call(['qemu-img', 'convert', file_path, raw_file_path])
            # TODO: Emit fedmsg?
            return raw_file_path
        except:
            print "Problem converting qcow2 file to raw."
            return None
    else:
        raise Exception("{0} is not a .qcow2 file.".format(file_path))
