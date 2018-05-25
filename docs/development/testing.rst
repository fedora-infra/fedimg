=======
Testing
=======

Fedimg provides a growing suite of unittests. The tests uses `pytest`_ Python
package.

Running the tests
-----------------

Virtualenv
++++++++++

Refer to the documentation to setup your virtualenv.

#. Activate the virtualenv::

    $ cd /path/to/fedimg/git/source
    $ source ./fedimg_env/bin/activate

#. Run the tests::

    $ python setup.py test

.. _pytest: https://pytest.org/


Vagrant box
+++++++++++

Vagrant allows contributors to get quickly up and running with a fedimg development environment by automatically configuring a virtual machine.
To get started, simply use these commands::

    $ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs
    $ sudo systemctl enable libvirtd
    $ sudo systemctl start libvirtd
    $ git clone git@github.com:fedora-infra/fedimg.git
    $ cd fedimg
    $ cp devel/Vagrantfile.example Vagrantfile
    $ vagrant up

You can ssh into your running Vagrant box like this::

    # Make sure your fedimg checkout is your shell's cwd
    $ vagrant ssh

The code from your development host will be mounted in ``/home/vagrant/fedimg``
in the guest. You can edit this code on the host, and the vagrant-sshfs plugin will cause the
changes to automatically be reflected in the guest's ``/home/vagrant/fedimg`` folder.

Run the tests::

    $ vagrant ssh
    $ cd fedimg
    $ tox