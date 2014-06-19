# Installation

The Fedimg installation process is rather straightforward and has been
successfully tested on Fedora 20.

## Install fedmsg components

`fedmsg-relay` allows Fedimg to send its own fedmsgs out to `fedmsg-hub`.

```
sudo yum install fedmsg-hub fedmsg-relay -y
sudo systemctl start fedmsg-relay
```

Running `fedmsg-hub` will print out fedmsgs as they are emitted by
the Fedora infrastructure. With `fedmsg-relay` running, Fedimg will
be able to send its own messages to the hub.

## Install the Koji library

The Koji library which provides access to the Fedora build system is not
pip-installable. Before starting Fedimg installation and setup, make sure
to install Koji with `sudo yum install koji`.

## Create a virtual environment

Once you've installed Koji, create a Python virtual environment that
includes the system-installed Koji library:

```
mkvirtualenv fedimg --system-site-packages
```

## Plug in the consumer

```
sudo cp fedmsg.d/fedimg.py /etc/fedmsg.d/fedimg.py
```
