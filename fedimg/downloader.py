#!/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import urllib2

# LOCAL_DOWNLOAD_DIR should be changed as appropriate in production
# in order to properly upload files to local shares for FTP access.
LOCAL_DOWNLOAD_DIR = "/var/lib/fedimg/download/"


def download(urls):
    """ Downloads files from a list of URLs with a progress bar and
    stores them locally. """

    # Create the proper local upload directory if it doesn't exist.
    if not os.path.exists(LOCAL_DOWNLOAD_DIR):
        os.makedirs(LOCAL_DOWNLOAD_DIR)

    print "Local downloads will be stored in {}.".format(LOCAL_DOWNLOAD_DIR)

    for url in urls:
        file_name = url.split('/')[-1]
        local_file_name = LOCAL_DOWNLOAD_DIR + file_name
        u = urllib2.urlopen(url)
        try:
            with open(local_file_name, 'wb') as f:
                meta = u.info()
                file_size = int(meta.getheaders("Content-Length")[0])

                print "Downloading {0} ({1} bytes)".format(url, file_size)
                bytes_downloaded = 0
                block_size = 8192
                while True:
                    buff = u.read(block_size)  # buffer
                    if not buff:
                        break

                    bytes_downloaded += len(buff)
                    f.write(buff)
                    bytes_remaining = float(bytes_downloaded) / file_size
                    status = r"{0}  [{1:.2%}]".format(bytes_downloaded,
                                                      bytes_remaining)
                    status = status + chr(8) * (len(status) + 1)
                    sys.stdout.write(status)
        except OSError:
            print "Problem writing to {}.".format(LOCAL_DOWNLOAD_DIR)
            print "Make sure to run this service with root permissions."
