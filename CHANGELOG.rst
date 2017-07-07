
0.7.5
-----

Pull Requests

- (@sayanchowdhury) #60, Snapshots in non us-east-1 don't get public
  https://github.com/fedora-infra/fedimg/pull/60

Commits

- d6f5457ff services.ec2: Make the snapshots in other regions public after run
  https://github.com/fedora-infra/fedimg/commit/d6f5457ff
- c5d6d2820 services.ec2: Use the alternate driver to query the regions
  https://github.com/fedora-infra/fedimg/commit/c5d6d2820
- 646a037a2 services.ec2: Add comment for the hack done for snapshots
  https://github.com/fedora-infra/fedimg/commit/646a037a2

0.7.4
-----

Pull Requests

- (@sayanchowdhury) #59, Retry till snapshot is public & Fix error handling.
  https://github.com/fedora-infra/fedimg/pull/59

Commits

- 0b3e6a0ca services.ec2: Fix the error handling in the EC2 Service
  https://github.com/fedora-infra/fedimg/commit/0b3e6a0ca
- d1f2d873e services.ec2: Keep retrying for making the snapshot public
  https://github.com/fedora-infra/fedimg/commit/d1f2d873e

0.7.3
-----

Pull Requests

- (@sayanchowdhury) #58, services.ec2: Log if the image was successfully made public
  https://github.com/fedora-infra/fedimg/pull/58

Commits

- 1acc5904d services.ec2: Log if the image was successfully made public
  https://github.com/fedora-infra/fedimg/commit/1acc5904d

0.7.2
-----

Pull Requests

- (@sayanchowdhury) #57, cron: Update the cron according to the upgrade notes
  https://github.com/fedora-infra/fedimg/pull/57

Commits

- a0de6182f cron: Update the cron according to the upgrade notes
  https://github.com/fedora-infra/fedimg/commit/a0de6182f

0.7.1
-----

Pull Requests

- (@sayanchowdhury) #53, Drop the 'os' and 'ver' from the configuration file. Related to #46
  https://github.com/fedora-infra/fedimg/pull/53
- (@sayanchowdhury) #55, Make the snapshots public so that AMIs can be copied to different accounts
  https://github.com/fedora-infra/fedimg/pull/55

Commits

- 985f9d8de Drop the 'os' and 'ver' from the configuration file. Related to #46
  https://github.com/fedora-infra/fedimg/commit/985f9d8de
- b25cc4f14 Make the snapshots public so that AMIs can be copied to different accounts
  https://github.com/fedora-infra/fedimg/commit/b25cc4f14

0.7
---

Pull Requests

- (@ralphbean)      #41, Setup logging for cronjob
  https://github.com/fedora-infra/fedimg/pull/41
- (@coolsvap)       #44, Update typos
  https://github.com/fedora-infra/fedimg/pull/44
- (@nishant-mor)    #46,  Dropped 'os' and 'ver' from the AWS_AMIS config
  https://github.com/fedora-infra/fedimg/pull/46
- (@ralphbean)      #47, Pungi4 fixes.
  https://github.com/fedora-infra/fedimg/pull/47
- (@ralphbean)      #49, Add a nice log statement at the beginning stating what we're going to upload.
  https://github.com/fedora-infra/fedimg/pull/49
- (@sayanchowdhury) #50, Fix to include nightly atomic uploads
  https://github.com/fedora-infra/fedimg/pull/50
- (@sayanchowdhury) #51, Migrate fedimg to compose based
  https://github.com/fedora-infra/fedimg/pull/51
- (@sayanchowdhury) #52, Send image raw_url to fedmsg instead of the build_name
  https://github.com/fedora-infra/fedimg/pull/52

Commits

- 60aa36b2a Setup logging for cronjob
  https://github.com/fedora-infra/fedimg/commit/60aa36b2a
- 511497384 Update typo in GCE service
  https://github.com/fedora-infra/fedimg/commit/511497384
- 6b9c3210d Update typo in rackspace service
  https://github.com/fedora-infra/fedimg/commit/6b9c3210d
- f470cebef Update typo in hp service
  https://github.com/fedora-infra/fedimg/commit/f470cebef
- 5a1c7ab51 Dropped 'os' and 'ver' from the AWS_AMIS config
  https://github.com/fedora-infra/fedimg/commit/5a1c7ab51
- 05452ed71 ex2.py : Added new format of AWS_AMIS config
  https://github.com/fedora-infra/fedimg/commit/05452ed71
- 20805fdd9 s/yum/dnf/
  https://github.com/fedora-infra/fedimg/commit/20805fdd9
- aec998075 Pungi4 fixes.
  https://github.com/fedora-infra/fedimg/commit/aec998075
- 9d4873858 Add a nice log statement at the beginning stating what we're going to upload.
  https://github.com/fedora-infra/fedimg/commit/9d4873858
- 156190880 Fix to include F24 nightly atomic uploads
  https://github.com/fedora-infra/fedimg/commit/156190880
- 335d2236a Migrate fedimg from koji-based to compose-based
  https://github.com/fedora-infra/fedimg/commit/335d2236a
- 7ae44d715 Minor fixes in the fedmsg consumer
  https://github.com/fedora-infra/fedimg/commit/7ae44d715
- a3a2300ab Change KojiConsumer to FedimgConsumer
  https://github.com/fedora-infra/fedimg/commit/a3a2300ab
- 1d0af12c1 Update the documenation to install fedfind while setting up
  https://github.com/fedora-infra/fedimg/commit/1d0af12c1
- 0e199c95d An small indentation typo resulting into major issue
  https://github.com/fedora-infra/fedimg/commit/0e199c95d
- 4f9e932f3 Send image raw_url to fedimg instead of the build_name
  https://github.com/fedora-infra/fedimg/commit/4f9e932f3

0.6.4
-----

Commits

- f94ade23f Typofix.
  https://github.com/fedora-infra/fedimg/commit/f94ade23f

0.6.3
-----

Pull Requests

- (@ralphbean)      #33, Rearrange image.test fedmsg alerts.
  https://github.com/fedora-infra/fedimg/pull/33
- (@ralphbean)      #40, Use new-style of accessing ec2 drivers.
  https://github.com/fedora-infra/fedimg/pull/40

Commits

- b5daa8ea3 Ignore eggs dir.
  https://github.com/fedora-infra/fedimg/commit/b5daa8ea3
- 99f51c92a Rearrange image.test fedmsg alerts.
  https://github.com/fedora-infra/fedimg/commit/99f51c92a
- 677410c59 Add a script that lists the latest AMIs from datagrepper.
  https://github.com/fedora-infra/fedimg/commit/677410c59
- 368816860 Closes #35, can kill any instance running more than 2 hours.
  https://github.com/fedora-infra/fedimg/commit/368816860
- 05b540390 Fixes the typo in the command name.
  https://github.com/fedora-infra/fedimg/commit/05b540390
- 9c230af02 Use new-style of accessing ec2 drivers.
  https://github.com/fedora-infra/fedimg/commit/9c230af02
- f891dccc9 Remove CHANGELOG header.
  https://github.com/fedora-infra/fedimg/commit/f891dccc9
- ddbb82523 Remove the spec file.  We keep it in Fedora dist-git.
  https://github.com/fedora-infra/fedimg/commit/ddbb82523


0.6
---

General

- Use a single threadpool for all uploads to avoid leaking threads
- Prevent major IndexError when checking Koji tasks that don't have raw.xz outputs
- Increase number of fedmsg endpoints

EC2Service

- Use larger and more powerful instance types for utility and test instances
- Typofix when naming PV images

Docs

- Add some basic contributor docs


0.5
---

EC2Service

- Use 7 GB volume size rather than 3 GB for now, since atomic images come out
  to be 6.1 GB
- Implement gp2 volume type uploads
- Image name now includes volume type
- Simplify consumer filter code, eliminating 32 bit stuff for now
- Add build name, virtualization type, and volume type to 'extra'
  dict in fedmsgs

Tests

- Fix up consumer test code
- Add additional consumer tests to test build filter code

Docs

- Add info about volume size configuration
- Tested on F21
- Improve index page
- Bring installation info up-to-date

Misc
- Commit atomic test script, to go with base test script
- Reduce description in setup.py


0.4
---

EC2Service

- Fix alternate destinations not being set properly during image copy
- Split util and test AMIs into dedicated lists
- Allow for URL redirection while curling raw.xz image
- Simplified registration AKI selection process
- Major refactoring to allow for future expansion into many different types of AMIs
- Uploads are now multithreaded
- Volume size options added to config options
- Better logging
- Close a dangling SSH connection (thanks, threebean!)
- Fix bug that caused only the first two AMIs to be made public

Tests

- Fix broken consumer test
- Committed `uploadtest.py` for doing EC2Service test runs during development

Docs

- Update messaging docs
- Add table of AMI types to EC2Service docs
- Add AMI config format info

Misc

- Removed extraneous EC2Service-specific stuff from other service files
- Better commenting


0.3.2
-----

- Use fedmsg logging utilities
- Convert old print statements to logging


0.3.1
-----

- Cycle through and make copied AMIs public after uploads complete
- Register AMI with description containing build name of source image file
- Report AMI Ids when emitting related fedmsgs
- Make sure all AMIs have a matching numerical extension across regions
- Clean up a little EC2Service code
- Typofixes, etc


0.3
---

- Add utility function to get virtualization type for EC2 AMI registration
- Make AMIs public after being tested and cpied
- Tweaks to layout of config file
- Only use 64 bit EBS utility instances
- Remove hardcoded username
- Rename some variables to be clearer
- add clean_up_on_failure and delete_image_on_failure config options
- Improve exception handling
- Make sure snapshot is deleted on cleanup if no image has been registered
- Add some starter tests
- Move around some processes to more appropriate files
- Don't attempt to provide an AKI when registering an image as HVM
- Fix root device name for PV vs. HVM
- Serious PEP 8 fixes
- Fix up duplicate image name prevention code
- Various typofixes and code cleanup


0.2.6
-----

- Use proper buildroot macro in spec file
- Preserve file timestamps when copying in spec file
- Do not make library files executable, and don't give them shebangs
- Add license headers to all Python files


0.2.5
-----

- Remove coding from fedmsg.d/fedimg.py since it seems to make it executable
- Make init file executable in spec install section, as well


0.2.4
-----

- Shorten spec summary and remove trailing dot
- Add shebang and coding to top of fedimg init file
- Remove shebang from fedmsg.d/fedimg.py
- Make all necessary fedimg files executable in spec install section


0.2.3
-----

- Better IAM profile name example in the config
- Addition to docs: section about setting up the config file
- Fix strange saces and add missing comma to setup.py classifiers section


0.2.2
-----

- Include .pyc and .pyo files for consumer in /etc/fedmsg.d/
- Add missing comma


0.2.1
-----

- Fix `packages` argument in setup.py to take `find_packages()`


0.2.0
-----

- Initial RPM release to Fedora
- setup.py improvements
- Config file is now read from /etc/fedimg.cfg
- PEP 8 fixes


0.1.0
-----

- Initial PyPI release

