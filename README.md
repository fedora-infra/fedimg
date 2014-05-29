# fedimg

Service to automatically upload built Fedora images to internal and external
cloud providers.

## License

AGPLv3+

## Requirements

Among the requirements listed in `setup.py` by `install_requires` is `koji`.
Koji is not available on PyPI. You must install the `koji` package to your
system via `sudo yum install koji` before creating a virtualenv, which you
should do with `mkvirtualenv [name] --system-site-packages` so that your
system install of `koji` is included with your virtualenv.

## Installation

Besides installing fedimg or before running `python setup.py {develop/install}`,
for now you must also copy `fedmsg/config.py` to
`/etc/fedmsg.d/kojiconsumer.py` in order for the consumer to properly listen in
on the fedmsg bus as `fedmsg-hub` (currently installed separately) runs.

## Providers

We hope to simultaneously upload our cloud images to a variety of internal and
external spaces.

### Current

None yet -- I've just started!

### Future

* Internal Fedora FTP server

* Amazon EC2

* GCE

* HP

* Rackspace

* Official internal Fedora and Red Hat cloud spaces

## Contributors

* David Gay [oddshocks@riseup.net]
