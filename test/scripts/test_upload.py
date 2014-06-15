#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg
import fedimg
import fedimg.services
from fedimg.services.ec2 import EC2Service, EC2ServiceException

ec2 = EC2Service()

ec2.upload('https://kojipkgs.fedoraproject.org//work/tasks/5144/6925144/fedora-cloud-base-rawhide-20140604.x86_64.raw.xz')
