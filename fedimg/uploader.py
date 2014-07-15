#!/bin/env python
# -*- coding: utf8 -*-

import koji

import fedimg
import fedimg.downloader
from fedimg.services.ec2 import EC2Service

from fedimg.util import get_qcow2_files


def upload(builds):
    """ Takes a list of one or more Koji build IDs (passed to it from
    consumer.py) and sends the appropriate image files off to cloud
    services. """

    # Create a Koji connection to the Fedora Koji instance
    koji_session = koji.ClientSession(fedimg.KOJI_SERVER)

    upload_files = list()  # list of full URLs of files

    if len(builds) == 1:
        task_result = koji_session.getTaskResult(builds[0])
        upload_files.append(get_rawxz_url(task_result))
    elif len(builds) >= 2:
        # Right now, builds only produce one .raw.xz file, so this should
        # never happen.
        koji.multicall = True
        for build in builds:
            koji_session.listTaskOutput(build)
        results = koji.multiCall()
        for result in results:
            upload_files.append(get_rawxz_url(result))

    # EC2 upload
    ec2 = EC2Service()
    for image in upload_files:
        # If the image is 32 bit and a base image
        # OR if it's 64 bit and an atomic or bigdata image,
        # then go ahead and upload the image
        if (image.find('i386') > -1
           and image.find('fedora-cloud-base') > -1) or \
           (image.find('x86_64') > -1
           and (image.find('fedora-cloud-atomic') > -1 or
                image.find('fedora-cloud-bigdata') > -1)):
            ec2.upload(image)
