#!/usr/bin/python
""" List the AMIs uploaded by fedimg in the last N days.

Deps:  $ sudo yum install python-requests

Author:     Ralph Bean <rbean@redhat.com>
License:    LGPLv2+
"""

from __future__ import print_function

import argparse
import collections
import datetime
import functools
import logging

import requests

log = logging.getLogger()

base_url = 'https://apps.fedoraproject.org/datagrepper/raw'
topic = "org.fedoraproject.prod.fedimg.image.upload"


def get_page(page, pages, delta):
    """ Retrieve the JSON for a particular page of datagrepper results """
    log.debug("Getting page %i of %s", page, pages)
    response = requests.get(base_url, params=dict(
        topic=topic,
        delta=delta,
        page=page,
    ))
    return response.json()


def desirable(msg, args):
    if not msg['msg']['status'] == 'completed':
        return False
    if args.rawhide and 'rawhide' not in msg['msg']['image_name']:
        return False
    if not args.rawhide and 'rawhide' in msg['msg']['image_name']:
        return False
    return True


def get_messages(args):
    """ Generator that yields messages from datagrepper """

    delta = int(datetime.timedelta(days=args.days).total_seconds())

    # Get the first page
    data = get_page(1, 'unknown', delta)
    for message in data['raw_messages']:
        if desirable(message, args):
            yield message

    more = functools.partial(get_page, pages=data['pages'], delta=delta)

    # Get all subsequent pages (if there are any...)
    for page in range(1, data['pages']):
        data = more(page + 1)

        for message in data['raw_messages']:
            if desirable(message, args):
                yield message


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--days', default=3, type=int,
        help="Number of days of history to search.  Default: 3")
    parser.add_argument(
        '-r', '--rawhide', action='store_true',
        help="Show rawhide instead of the branched (pre-)release")
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="Produce lots of output")

    return parser.parse_args()


if __name__ == '__main__':
    # 1 - Initialize
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # 2 - Build a results dict
    results = collections.OrderedDict()
    messages = get_messages(args)
    for message in messages:
        key = message['msg']['image_name']
        if not key in results:
            results[key] = []
        results[key].append(message['msg'])

    # 3 - Print it out and format it
    for key, uploads in results.items():
        for upload in uploads:
            extra = upload['extra']
            print(
                key.ljust(45),
                upload.get('destination', '').ljust(20),
                extra.get('id', '').ljust(15),
                extra.get('virt_type', '').ljust(13),
                extra.get('vol_type', '').ljust(15),
            )
