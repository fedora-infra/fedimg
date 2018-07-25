=============
Release Notes
=============

2.3.0
=====

Developer Improvements
----------------------

* tests: Fix the tests for the broken links
  (`#151 <https://github.com/fedora-infra/fedimg/pull/151>`_).
* utils: Fix the tests for the travis test failures
  (`#152 <https://github.com/fedora-infra/fedimg/pull/152>`_).
* setup: Update the AUTHORS & the AUTHORS EMAIL in setup.py
  (`#153 <https://github.com/fedora-infra/fedimg/pull/153>`_).

Bug fixes
---------

* config: Fix the config to pick local if needed
  (`#150 <https://github.com/fedora-infra/fedimg/pull/150>`_).

Contributors
------------

The following developers contributed patches to Fedimg 2.2.0:

- Sayan Chowdhury

2.2.0
=====

Developer Improvements
----------------------

* utils: Cancel the conversion tasks if the are older then 24 hours
  (`#146 <https://github.com/fedora-infra/fedimg/pull/146>`_).

Contributors
------------

The following developers contributed patches to Fedimg 2.2.0:

- Sayan Chowdhury

2.1.0
=====

Bug fixes
---------

* Fix the version and release number in sphinx conf
  (`#133 <https://github.com/fedora-infra/fedimg/pull/133>`_).

Developer Improvements
----------------------

* Support both type of resource ids (long & short)
  (`#141 <https://github.com/fedora-infra/fedimg/pull/141>`_).
* Migrate fedimg to support to longer resource ids
  (`#137 <https://github.com/fedora-infra/fedimg/pull/137>`_).

Contributors
------------

The following developers contributed patches to Fedimg 2.1.0:

- Sayan Chowdhury

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
