Fedimg provides a growing suite of unittests that can be run with the
`nosetests` command provided by the `nose` Python package.

## Setup

Running `python setup.py test` from within your virtualenv will install any
packages required by the test suite, including `nose`.

Tests are best run with the `nosetests` command while inside your virtualenv.

**Note**: Getting an error regarding a missing module when running `nosetests`
can be caused by `nose` not being run with the virtualenv's library set. This
can be resolved by running the tests with ``python `which nosetests` ``,
instead of simply `nosetests`. If you get missing module errors for `nose` or
`mock`, you may first have to force the required testing
libraries into your virtualenv by running `pip install nose mock -I`.
