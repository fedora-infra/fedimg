
## 0.6

**General**
-   use a single threadpool for all uploads to avoid leaking threads
-   prevent major IndexError when checking Koji tasks that don't have raw.xz
    outputs
-   increase number of fedmsg endpoints

**EC2Service**
-   use larger and more powerful instance types for utility and test instances
-   typofix when naming PV images

**Docs**
-   add some basic contributor docs

## 0.5

**EC2Service**
-   use 7 GB volume size rather than 3 GB for now, since atomic images come out
    to be 6.1 GB
-   implement gp2 volume type uploads
-   image name now includes volume type
-   simplify consumer filter code, eliminating 32 bit stuff for now
-   add build name, virtualization type, and volume type to 'extra'
    dict in fedmsgs

**Tests**
-   fix up consumer test code
-   add additional consumer tests to test build filter code

**Docs**
-   add info about volume size configuration
-   "tested on F21"
-   improve index page
-   bring installation info up-to-date

**Misc**
-   commit atomic test script, to go with base test script
-   reduce description in setup.py

## 0.4

**EC2Service**
-   fix alternate destinations not being set properly during image copy
-   split util and test AMIs into dedicated lists
-   allow for URL redirection while curling raw.xz image
-   simplified registration AKI selection process
-   major refactoring to allow for future expansion into many different
    types of AMIs
-   uploads are now multithreaded
-   volume size options added to config options
-   better logging
-   close a dangling SSH connection (thanks, threebean!)
-   fix bug that caused only the first two AMIs to be made public

**Tests**
-   fix broken consumer test
-   committed `uploadtest.py` for doing EC2Service test runs during
    development

**Docs**
-   update messaging docs
-   add table of AMI types to EC2Service docs
-   add AMI config format info

**Misc**
-   removed extraneous EC2Service-specific stuff from other service files
-   better commenting

## 0.3.2

-   use fedmsg logging utilities
-   convert old print statements to logging

## 0.3.1

-   cycle through and make copied AMIs public after uploads complete
-   register AMI with description containing build name of source image file
-   report AMI Ids when emitting related fedmsgs
-   make sure all AMIs have a matching numerical extension across regions
-   clean up a little EC2Service code
-   typofixes, etc

## 0.3

-   add utility function to get virtualization type for EC2 AMI registration
-   make AMIs public after being tested and cpied
-   tweaks to layout of config file
-   only use 64 bit EBS utility instances
-   remove hardcoded username
-   rename some variables to be clearer
-   add clean_up_on_failure and delete_image_on_failure config options
-   improve exception handling
-   make sure snapshot is deleted on cleanup if no image has been registered
-   add some starter tests
-   move around some processes to more appropriate files
-   don't attempt to provide an AKI when registering an image as HVM
-   fix root device name for PV vs. HVM
-   serious PEP 8 fixes
-   fix up duplicate image name prevention code
-   various typofixes and code cleanup

## 0.2.6

-   use proper buildroot macro in spec file
-   preserve file timestamps when copying in spec file
-   do not make library files executable, and don't give them shebangs
-   add license headers to all Python files 

## 0.2.5

-   Remove coding from fedmsg.d/fedimg.py since it seems to make it executable
-   make init file executable in spec install section, as well

## 0.2.4

-   Shorten spec summary and remove trailing dot
-   Add shebang and coding to top of fedimg init file
-   Remove shebang from fedmsg.d/fedimg.py
-   Make all necessary fedimg files executable in spec install section

## 0.2.3

-   Better IAM profile name example in the config
-   Addition to docs: section about setting up the config file
-   Fix strange saces and add missing comma to setup.py classifiers section

## 0.2.2

-   Include .pyc and .pyo files for consumer in /etc/fedmsg.d/
-   Add missing comma

## 0.2.1

-   Fix `packages` argument in setup.py to take `find_packages()`

## 0.2.0

-   Initial RPM release to Fedora
-   setup.py improvements
-   Config file is now read from /etc/fedimg.cfg
-   PEP 8 fixes

## 0.1.0

-   Initial PyPI release

