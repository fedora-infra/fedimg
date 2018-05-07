=============
Release Notes
=============


2.0.0
=====

Deprecation
-----------

* The fedmsg message ``fedimg.image.upload`` has been deprecated for all other
  regions other than the ``base_region``
  (`#97 <https://github.com/fedora-infra/fedimg/pull/97>`_).


Bug fixes
---------

* Refactor the ``FedimgConsumer`` to handle F28 Two week Atomic
  (`#123 <https://github.com/fedora-infra/fedimg/pull/123>`_).

Developer Improvements
----------------------

* Fix the tests for ``utils.py``
  (`#124 <https://github.com/fedora-infra/fedimg/pull/124>`_).
* Fix the FSF address in setup.py messed up during the version bump
  (`#127 <https://github.com/fedora-infra/fedimg/pull/127>`_).
* Migrate from nose to pytest
  (`#128 <https://github.com/fedora-infra/fedimg/pull/128>`_).
* Fix the filename type for CHANGELOG.rst
  (`#129 <https://github.com/fedora-infra/fedimg/pull/129>`_).
* Raise exceptions when shell execution fails
  (`#130 <https://github.com/fedora-infra/fedimg/pull/130>`_).
* Refactor the docs to use sphinx, and update the latest architecture
  (`#131 <https://github.com/fedora-infra/fedimg/pull/131>`_).

Contributors
------------

The following developers contributed patches to Fedimg 2.0.0:

- Sayan Chowdhury
