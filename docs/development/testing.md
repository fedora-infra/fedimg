# Testing

Fedimg provides a growing suite of unittests that can be run with the
`nosetests` command provided by the `nose` Python package.

## Setup

Running `python setup.py test` from within your virtualenv will install any
packages required by the test suite, including `nose`.

Tests are best run with the `nosetests` command while inside your virtualenv.

**Note**: Getting an error regarding a missing module when running `nosetests`
can be caused by `nose` not being run with the virtualenv's library set. This
can be resolved by running the tests with ``python `which nosetests` ``,
instead of simply `nosetests`. If you don't want to have to type the longer
command every time, you can make the tests run properly via simply `nosetests`
by first running `alias nosetests="/usr/bin/env python $(which nosetests)`. For
even more permanence, add that `alias` line to your `~/.zshrc`, `~/.bashrc`, or
other profile configuration. *Remember:* If you choose to modify one of these
configuration files, you will need to run `source` on the file for the changes
to take effect.
