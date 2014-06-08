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

    # Download files locally and compress them with xz.
    # download() returns raw image files made from the downloaded qcow2s
    raw_images = fedimg.downloader.download(upload_files)

    # EC2 upload
    ec2 = EC2Service()
    for image in raw_images:
        ec2.upload(image)
