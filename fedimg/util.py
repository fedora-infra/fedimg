#!/bin/env python
# -*- coding: utf8 -*-
"""
Utility functions for fedimg.
"""

import subprocess

import fedimg


def get_file_arch(file_name):
    """ Takes a file name (probably of a .raw.xz image file) and returns
    the suspected architecture of the contained image. If it doesn't look
    like a 32-bit or 64-bit image, None is returned. """
    if file_name.find('i386') != -1:
        return 'i386'
    elif file_name.find('x86_64') != -1:
        return 'x86_64'
    else:
        return None


def get_rawxz_url(task_result):
    """ Returns the URL of the raw.xz file produced by the Koji
    task ID represented by the task_result argument. """
    # I think there might only ever be one qcow2 file per task,
    # but doing it this way plays it safe.
    file_name = [f for f in task_result['files'] if f.endswith('.raw.xz')][0]
    task_id = task_result['task_id']

    # extension to base URL to exact file directory
    koji_url_extension = "/{}/{}".format(str(task_id)[3:], str(task_id))
    full_file_location = fedimg.BASE_KOJI_TASK_URL + koji_url_extension

    return full_file_location + "/{}".format(file_name)


def compress(file_path):
    """ DEPRECATED
    Compress a downloaded image file into a tar.xz file. Deletes the
    original file and returns file path to compressed file. """
    xz_file_path = file_path + ".tar.xz"
    subprocess.call(['tar', '-cfJ', xz_file_path, file_path])
    # Above command waits until command completes before returning,
    # there shouldn't need to be any wait() method called.
    subprocess.call(['rm', file_path])
    return xz_file_path


def get_qcow2_files(task_result):
    """ DEPRECATED
    Returns a list of URLs to qcow2 files produced by the Koji
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
    """ DEPRECATED
    Takes the file path of a qcow2 image file and creates a .raw conversion
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
