.. Fedimg documentation master file, created by
   sphinx-quickstart on Sat May  5 00:26:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======
Fedimg
======

Fedimg is a `Python`_-powered service that is built
to make Fedora Cloud and Atomic Host images available on popular cloud
providers, such as `Amazon Web Services`_.

Salient features:

* Performs automatic uploads, triggered by activity on the `Fedmsg`_ bus.
* Register images as Hardware Virtual Machine (HVM).
* Emits fedmsg messages, providing the upload status and the Amazon Machine
  Image (AMI) info.
* Packaged for EPEL7, Fedora as well as PyPI.

License
=======
Fedimg is licensed under the AGPL, version 3 or later.

Contents:

.. toctree::
   :maxdepth: 2

   architecture/configuration
   architecture/consumer
   development/installation
   development/contribution
   development/testing

.. toctree::
   :maxdepth: 1

   release_notes

Community
=========

Fedimg is maintained by the Fedora Project and it's `source code`_ and `issue
tracker`_ are on Github. Join the `mailing list`_ or/and the IRC
channel on `FreeNode`_, ``#fedora-cloud`` for discussion on Fedimg.

.. _Python: https://www.python.org/
.. _Amazon Web Services: https://aws.amazon.com/
.. _source code: https://github.com/fedora-infra/fedimg
.. _mailing list: https://lists.fedoraproject.org/admin/lists/infrastructure.lists.fedoraproject.org/
.. _FreeNode: https://freenode.net/
.. _fedmsg: http://www.fedmsg.com
.. _issue tracker: https://github.com/fedora-infra/fedimg/issues/

