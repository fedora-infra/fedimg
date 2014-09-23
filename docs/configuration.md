# Configuration

The Fedimg service pulls its configuration variables from the file located at
`/etc/fedimg.cfg`. The file `fedimg.cfg.example` included with Fedimg can be
used as a starting point for writing your own configuration file.

At the time of this writing, the configuration file is read in when Fedimg is
initialized, so it may be necessary to restart Fedimg after making a
configuration change.
