# fedimg

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

Besides installing fedimg or before running `python setup.py {develop/install}`,
for now you must also copy `fedmsg/config.py` to
`/etc/fedmsg.d/kojiconsumer.py` in order for the consumer to properly listen in
on the fedmsg bus as `fedmsg-hub` (currently installed separately) runs.

## Providers

We hope to simultaneously upload our cloud images to a variety of internal and
external spaces.

### Current

* Local file downloads (to be sent, for example, to an NFS share to make the
  image files available on Fedora's internal FTP server

### Future

* Amazon EC2

* GCE

* HP

* Rackspace

* Official Fedora and Red Hat cloud spaces

## Contributors

* David Gay [oddshocks@riseup.net]

* Ralph Bean [rbean@redhat.com]
