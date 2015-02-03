Fedimg is a [Python](https://www.python.org/)-powered service that was built to
make [Fedora Cloud]() images available on popular cloud providers, such as
Amazon Web Services (AWS), Rackspace, and Google Compute Engine (GCE). It runs
on the [Fedora infrastructure](), where it takes advantage of
[Fedmsg](http://www.fedmsg.com/en/latest/). Fedimg saves Fedora engineers and
developers from having to manually register every newly built Fedora Cloud
image with cloud providers. Every base or atomic Fedora Cloud image
successfully built in [Koji](http://koji.fedoraproject.org/koji/) is picked up
by Fedimg -- whether it's a development build or an official release.

## Features

-   Automatic uploads, triggered by activity on the Fedmsg bus

-   Registers images as both paravirtual and HVM, when appropriate

-   Images with names containing 'atomic' are treated as
    [Atomic](http://www.projectatomic.io/) images, and registered as such

-   All "heavy lifting" (like downloading and uncompressing raw images) is
    done ~in the cloud~

-   Emits fedmsgs, providing upload status and image info

-   Works with AWS EC2, with additional services to be added in the future

-   Packaged for EPEL 7 (`yum install python-fedimg`) and available [on
    PyPI](https://pypi.python.org/pypi/fedimg/)

## License

Fedimg is licensed under the AGPL, version 3 or later. See the source code for
the [full license
text](https://github.com/fedora-infra/fedimg/blob/develop/LICENSE).

## Authors

Fedimg was written by David Gay, with contributions from Ralph Bean.
