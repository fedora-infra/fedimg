Fedimg is packaged for EPEL 7. The latest version been tested on RHEL 7 and
Fedora 22.

## Installing to the system

Install Fedimg with dnf (or yum):

```
sudo dnf install python-fedimg
```

The configration file should be found at `/etc/fedimg.cfg`. You will have to
modify this file before Fedimg will work. Read [the configuration
docs](configuration.md) for more info.

## Installing to a virtualenv

Make sure koji and fedfind is installed on your system:

```
sudo dnf install koji fedfind
```

Create a virtualenv that includes the system install of koji:

```
mkvirtualenv --system-site-packages fedimg
```

Install the fedmsg file:

```
cp fedmsg.d/fedimg.py /etc/fedmsg.d/fedimg.py
```

From inside the virtualenv, run the setup file:

```
python setup.py develop
```

Make sure `fedmsg-relay` is installed and started:

```
sudo dnf install fedmsg-relay
sudo systemctl start fedmsg-relay
```

Finally, a configuration file needs to exist at `/etc/fedimg.cfg`.
An example is provided with Fedimg as `fedimg.cfg.example`. You
can modify this file for your purposes and then copy it to `/etc/`.
Read [the configuration docs](configuration.md) for more info.
