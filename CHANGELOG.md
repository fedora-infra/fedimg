# Changelog

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

