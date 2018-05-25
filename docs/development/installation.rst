=================
Development Guide
=================

A vagrant virtual machine is avalaible to make running the unit test easy. If you wish to use this virual machine as development environment
you can check how to get started in the `testing documentation`_.


Fedimg is application written in Python. It uses `libcloud`_ to connect with
the external Cloud providers.

#. Clone the repository from Github::

    $ git clone git@github.com:fedora-infra/fedimg.git

#. Installing the dependencies::

    $ virtualenv fedimg_env
    $ source ./fedimg_env/bin/activate
    $ python setup.py develop

#. Setting up the configuration::

    $ mkdir -p /etc/fedimg/
    $ cp fedimg-conf.toml.example /etc/fedimg/fedimg-conf.toml

#. Setup AWS credentials

    Update the values of ``access_id`` and ``secret_key`` with your AWS tokens in
    ``/etc/fedimg/fedimg-conf.toml`` file.

#. Setup the euca2ools configuration::

    $ mkdir ~/.euca
    $ cp euca-fedimg.ini ~/.euca/config.ini

#. Setup the euc2ools credentials

    Update the values of ``key-id`` and ``secret-key`` with your AWS tokens in the
    ``~/.euca/config.ini`` file.

#. Run the fedmsg-hub::

    $ fedmsg-hub

Happy Hacking!

.. _libcloud: https://libcloud.apache.org/
.. _testing documentation:  https://github.com/fedora-infra/fedimg/blob/develop/docs/development/testing.rst