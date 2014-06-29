#!/bin/env python
# -*- coding: utf8 -*-

import fedmsg
import fedimg
import fedimg.services
from fedimg.services.ec2 import EC2Service, EC2ServiceException

ec2 = EC2Service()

ec2.upload('https://kojipkgs.fedoraproject.org//work/tasks/9442/7049442/fedora-cloud-base-20140616-rawhide.x86_64.raw.xz')
