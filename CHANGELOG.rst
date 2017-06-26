
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
