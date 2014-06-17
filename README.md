# Fedimg

Service to automatically upload built Fedora images to internal and external
cloud providers.

## License

AGPLv3+

## Requirements

Besides the requirements listed in `setup.py` by `install_requires` is the
`koji` module.  Koji is not available on PyPI. You must install the `koji`
package to your system via `sudo yum install koji` before creating a
virtualenv for fedimg, which you should do with `mkvirtualenv [name]
--system-site-packages` so that your system install of `koji` is included with
your virtualenv.

## Installation

Besides installing fedimg or before running `python setup.py
{develop/install}`, you must copy `fedmsg.d/fedimg.py` to
`/etc/fedmsg.d/fedimg.py` in order for the consumer to properly listen in on
the fedmsg bus as `fedmsg-hub` (currently installed separately) runs.

## Providers

We hope to simultaneously upload our cloud images to a variety of internal and
external spaces. Currently, the code supports Amazon EC2. Work has begun
toward supporting Rackspace, GCE, and HP. We're currently waiting on some
legal developments to determine what sort of account and access we'll have
to these providers.

## Contributors

* David Gay <oddshocks@riseup.net>

* Ralph Bean <rbean@redhat.com>
