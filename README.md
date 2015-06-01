# Fedimg

Service to automatically upload built Fedora images to internal and external
cloud providers.

## License

Fedimg is licensed under AGPLv3 or newer. See the `LICENSE` file for more
information.

## Documentation

Official Fedimg documentation can be [found at
RTFD](https://fedimg.readthedocs.org) or in `docs/`.

## Triggering jobs

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

## Providers

We hope to simultaneously upload our cloud images to a variety of internal and
external spaces. Currently, the code supports Amazon EC2. Work has begun
toward supporting Rackspace, GCE, and HP. We're currently waiting on some
legal developments to determine what sort of account and access we'll have
to these providers.

## Contributors

* David Gay <dgay@redhat.com>

* Ralph Bean <rbean@redhat.com>
