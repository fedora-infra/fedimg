#!/bin/env python
# -*- coding: utf8 -*-

"""
You must have fedmsg-relay installed to your system and started
via `systemctl start fedmsg-relay` in order to use this script.
"""

import fedmsg
import requests

fedmsg.init(active=True, name="relay_inbound")

idx = '2014-707e188d-fc5e-4c9a-a4a2-9499beaafffe'

resp = requests.get('https://apps.fedoraproject.org/datagrepper/id?id=%s' % idx)
msg = resp.json()

tokens = msg['topic'].split('.')
modname = tokens[4]
topic = '.'.join(tokens[5:])

print "Faking {}\n".format('.'.join(tokens))

fedmsg.publish(modname=modname, topic=topic, msg=msg['msg'])
