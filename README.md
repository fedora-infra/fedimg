# Fedimg

Service to automatically upload built Fedora images to internal and external
cloud providers.

## License

AGPLv3+

## Documentation

Official Fedimg documentation can be [found at
RTFD](https://fedimg.readthedocs.org). This readme contains at least the basic
information needed to set up Fedimg.

### Requirements

Besides the requirements listed in `setup.py` by `install_requires` is the
`koji` module. Koji is not available on PyPI. You must install the `koji`
package to your system via `sudo yum install koji` before creating a
virtualenv for fedimg, which you should do with `mkvirtualenv [name]
--system-site-packages` so that your system install of `koji` is included with
your virtualenv.

### Installation

Besides installing fedimg or before running `python setup.py
{develop/install}`, you must copy `fedmsg.d/fedimg.py` to
`/etc/fedmsg.d/fedimg.py` in order for the consumer to properly listen in on
the fedmsg bus as `fedmsg-hub` (currently installed separately) runs. You
should also make sure that `fedmsg-relay` is installed with `yum` and
started with `sudo systemctl start fedmsg-relay` so that Fedimg can
emit its own fedmsgs.

### Triggering jobs

Fedimg is designed to perform automatically when it sees the appropriate
fedmsg. However, sometimes, it's useful to be able to quickly trigger
a job manually. If Fedimg is installed properly, the `bin/trigger_upload.py`
script can be used for this purpose:

```
./bin/trigger_upload.py SOME_RAWXZ_URL
```

This script simply skips the part where Fedimg listens for the fedmsg, and
allows you to directly provide a URL to a raw.xz image file that you'd like
uploaded. Otherwise, Fedimg performs the same as during automatic operation.

### Providers

We hope to simultaneously upload our cloud images to a variety of internal and
external spaces. Currently, the code supports Amazon EC2. Work has begun
toward supporting Rackspace, GCE, and HP. We're currently waiting on some
legal developments to determine what sort of account and access we'll have
to these providers.

## Contributors

* David Gay <dgay@redhat.com>

* Ralph Bean <rbean@redhat.com>
