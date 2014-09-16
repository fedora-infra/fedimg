# Changelog

## 0.1.0

-   Initial PyPI realease

## 0.2.0

-   Initial RPM release to Fedora
-   setup.py improvements
-   Config file is now read from /etc/fedimg.cfg
-   PEP 8 fixes

## 0.2.1

-   Fix `packages` argument in setup.py to take `find_packages()`

## 0.2.2

-   Include .pyc and .pyo files for consumer in /etc/fedmsg.d/
-   Add missing comma

## 0.2.3

-   Better IAM profile name example in the config
-   Addition to docs: section about setting up the config file
-   Fix strange saces and add missing comma to setup.py classifiers section

## 0.2.4

-   Shorten spec summary and remove trailing dot
-   Add shebang and coding to top of fedimg init file
-   Remove shebang from fedmsg.d/fedimg.py
-   Make all necessary fedimg files executable in spec install section
