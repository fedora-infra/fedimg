#!/bin/env python
# -*- coding: utf8 -*-

import os
import subprocess
import sys
import urllib2

import fedimg
import fedimg.messenger

from fedmsg.util import compress


def download(urls):
    """ Downloads files from a list of URLs with a progress bar and
    stores them locally. """

    # Create the proper local upload directory if it doesn't exist.
    if not os.path.exists(fedimg.LOCAL_DOWNLOAD_DIR):
        os.makedirs(fedimg.LOCAL_DOWNLOAD_DIR)

    print "Local downloads will be stored in {}.".format(
        fedimg.LOCAL_DOWNLOAD_DIR)

    for url in urls:
        file_name = url.split('/')[-1]
        local_file_name = fedimg.LOCAL_DOWNLOAD_DIR + file_name
        u = urllib2.urlopen(url)
        try:
            with open(local_file_name, 'wb') as f:
                meta = u.info()
                file_size = int(meta.getheaders("Content-Length")[0])

                print "Downloading {0} ({1} bytes)".format(url, file_size)
                bytes_downloaded = 0
                block_size = 8192
                fedimg.messenger.message(file_name,
                                         'internal Fedora FTP',
                                         'started')
                while True:
                    buff = u.read(block_size)  # buffer
                    if not buff:
                        try:
                            compress(local_file_name)
                        except OSError:
                            print "ERROR: Problem compressing image file."
                            # TODO: Do we still want this sort of failure
                            # message if the file downloaded properly
                            # but failed to compress?
                            fedimg.messenger.message(file_name,
                                                     'internal Fedora FTP',
                                                     'failed')
                            break

                        fedimg.messenger.message(file_name,
                                                 'internal Fedora FTP',
                                                 'succeeded')
                        break

                    bytes_downloaded += len(buff)
                    f.write(buff)
                    bytes_remaining = float(bytes_downloaded) / file_size
                    if fedimg.DOWNLOAD_PROGRESS:
                        # TODO: Improve this progress indicator by making
                        # it more readable and user-friendly.
                        status = r"{0}  [{1:.2%}]".format(bytes_downloaded,
                                                          bytes_remaining)
                        status = status + chr(8) * (len(status) + 1)
                        sys.stdout.write(status)
        except OSError:
            print "Problem writing to {}.".format(fedimg.LOCAL_DOWNLOAD_DIR)
            print "Make sure to run this service with root permissions."
            fedimg.messenger.message(file_name, 'internal Fedora FTP',
                                     'failed')
