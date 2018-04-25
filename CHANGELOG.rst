
1.3.0
-----

Pull Requests

- (@sayanchowdhury) #103, consumers: Fix the metadata handling for Rawhide messages
  https://github.com/fedora-infra/fedimg/pull/103
- (@dustymabe)      #104, fix trace for incorrect log function call
  https://github.com/fedora-infra/fedimg/pull/104
- (@sayanchowdhury) #100, services.ec2: Check if the AMI is complete before proceeding
  https://github.com/fedora-infra/fedimg/pull/100
- (@sayanchowdhury) #117, services.ec2: Fix the ImportError in ec2imguploader
  https://github.com/fedora-infra/fedimg/pull/117
- (@sayanchowdhury) #112, services.ec2: Delete the source for every image urls
  https://github.com/fedora-infra/fedimg/pull/112
- (@sinnykumari)    #116, Don't use extend() when object is NoneType
  https://github.com/fedora-infra/fedimg/pull/116
- (@sinnykumari)    #111, Include AMIs to missing AWS ec2 regions
  https://github.com/fedora-infra/fedimg/pull/111
- (@sayanchowdhury) #99, utils: Extract the raw first before processing
  https://github.com/fedora-infra/fedimg/pull/99

Commits

- cf00cbedd consumers: Fix the metadata handling for Rawhide messages
  https://github.com/fedora-infra/fedimg/commit/cf00cbedd
- b3441f12f fix trace for incorrect log function call
  https://github.com/fedora-infra/fedimg/commit/b3441f12f
- 9170b0d60 services.ec2: Check if the AMI is complete before proceeding
  https://github.com/fedora-infra/fedimg/commit/9170b0d60
- d82da63f1 Include AMIs to missing AWS ec2 regions
  https://github.com/fedora-infra/fedimg/commit/d82da63f1
- 722151591 Don't use extend() when object is NoneType
  https://github.com/fedora-infra/fedimg/commit/722151591
- b3dd56e51 services.ec2: Fix the ImportError in ec2imguploader
  https://github.com/fedora-infra/fedimg/commit/b3dd56e51
- bf6450c7c services.ec2: Delete the source for every image urls
  https://github.com/fedora-infra/fedimg/commit/bf6450c7c
- 6ad790b65 utils: Extract the raw first before processing
  https://github.com/fedora-infra/fedimg/commit/6ad790b65

1.2.0
-----

Pull Requests

- (@sayanchowdhury) #85, consumer: Support F28 Atomic & Cloud messages
  https://github.com/fedora-infra/fedimg/pull/85
- (@sayanchowdhury) #86, services.ec2: Fix the volume_type attribute
  https://github.com/fedora-infra/fedimg/pull/86
- (@sayanchowdhury) #87, services.ec2: Add the missing push_notifications args
  https://github.com/fedora-infra/fedimg/pull/87
- (@sayanchowdhury) #89, scripts: Remove script to delete the ec2 nodes
  https://github.com/fedora-infra/fedimg/pull/89
- (@sayanchowdhury) #88, services.ec2: Send a image.upload message when completed
  https://github.com/fedora-infra/fedimg/pull/88
- (@sayanchowdhury) #90, consumers: Ignore the Unsupported releases
  https://github.com/fedora-infra/fedimg/pull/90
- (@sayanchowdhury) #92, fedimg: Include the image_url in fedmsg messages
  https://github.com/fedora-infra/fedimg/pull/92
- (@sayanchowdhury) #93, scripts: Fix the script to send proper format of compose id
  https://github.com/fedora-infra/fedimg/pull/93
- (@sayanchowdhury) #91, Change to use of consistent logging variables
  https://github.com/fedora-infra/fedimg/pull/91
- (@sayanchowdhury) #96, fedimg: Fix the script function argument order
  https://github.com/fedora-infra/fedimg/pull/96
- (@sayanchowdhury) #94, utils: Don't change the name of the image, breaks the get_ami.py layout
  https://github.com/fedora-infra/fedimg/pull/94

Commits

- b252bc483 consumer: Support F28 Atomic & Cloud messages
  https://github.com/fedora-infra/fedimg/commit/b252bc483
- 15e41e51f logging: Change the source to consistent logging
  https://github.com/fedora-infra/fedimg/commit/15e41e51f
- 8e8f22dd9 tests: Fix the tests for the consistent logging change
  https://github.com/fedora-infra/fedimg/commit/8e8f22dd9
- 307ce0bb0 scripts: Remove script to delete the ec2 nodes
  https://github.com/fedora-infra/fedimg/commit/307ce0bb0
- 161a0e15c services.ec2: Fix the volume_type attribute
  https://github.com/fedora-infra/fedimg/commit/161a0e15c
- 7355a5cb7 services.ec2: Add the missing push_notifications args
  https://github.com/fedora-infra/fedimg/commit/7355a5cb7
- 6ac912293 services.ec2: Send a image.upload message when completed
  https://github.com/fedora-infra/fedimg/commit/6ac912293
- 7fc9c32c4 consumers: Ignore the Unsupported releases
  https://github.com/fedora-infra/fedimg/commit/7fc9c32c4
- e21f70dbc fedimg: Include the image_url in fedmsg messages
  https://github.com/fedora-infra/fedimg/commit/e21f70dbc
- 3b9a86bdb scripts: Fix the script to send proper format of compose id
  https://github.com/fedora-infra/fedimg/commit/3b9a86bdb
- de4af7935 fedimg: Fix the script function args
  https://github.com/fedora-infra/fedimg/commit/de4af7935
- 3946ed1c3 utils: Don't change the name of the image, breaks the get_ami.py layout
  https://github.com/fedora-infra/fedimg/commit/3946ed1c3

1.1.0
-----

Pull Requests

- (@sayanchowdhury) #66, consumer: fedfind has deprecated `get_release_cid` method.
  https://github.com/fedora-infra/fedimg/pull/66
- (@sayanchowdhury) #67, scripts: Fix the manual upload trigger script
  https://github.com/fedora-infra/fedimg/pull/67
- (@sayanchowdhury) #68, fedimg: Remove redundant ec2.py file
  https://github.com/fedora-infra/fedimg/pull/68
- (@sayanchowdhury) #76, scripts: Update the trigger_upload, and remove redundant code
  https://github.com/fedora-infra/fedimg/pull/76
- (@sayanchowdhury) #75, Initial tests for fedimg
  https://github.com/fedora-infra/fedimg/pull/75
- (@euank)          #77, Fix numerous dependency issues, fix broken unit tests, add travis ci config
  https://github.com/fedora-infra/fedimg/pull/77
- (@sayanchowdhury) #79, services.ec2: Change the bucket name to more related to fedimg
  https://github.com/fedora-infra/fedimg/pull/79
- (@puiterwijk)     #80, Error out if starting the task failed
  https://github.com/fedora-infra/fedimg/pull/80
- (@sayanchowdhury) #70, fedimg.ec2: Add metadata to the `image.copy` fedmsg message
  https://github.com/fedora-infra/fedimg/pull/70
- (@sayanchowdhury) #81, services.ec2: Deprecate the PV images
  https://github.com/fedora-infra/fedimg/pull/81
- (@sayanchowdhury) #69, fedimg.ec2: Add the support for Elastic Network Adapter
  https://github.com/fedora-infra/fedimg/pull/69
- (@sayanchowdhury) #82, uploader: Set push_notifications to True when automatic upload
  https://github.com/fedora-infra/fedimg/pull/82
- (@sayanchowdhury) #84, Update the trigger_upload.py script to add push_notifications
  https://github.com/fedora-infra/fedimg/pull/84

Commits

- 84d0d69ef consumer: fedfind has deprecated `get_release_cid` method.
  https://github.com/fedora-infra/fedimg/commit/84d0d69ef
- 7bdd06f56 scripts: Fix the manual upload trigger script
  https://github.com/fedora-infra/fedimg/commit/7bdd06f56
- 33a86b79b fedimg: Remove redundant ec2.py file
  https://github.com/fedora-infra/fedimg/commit/33a86b79b
- b0fa1c4f9 tests: Fix the test for consumers
  https://github.com/fedora-infra/fedimg/commit/b0fa1c4f9
- e082ad464 tests: Add tests for the fedimg.uploader
  https://github.com/fedora-infra/fedimg/commit/e082ad464
- 1788e9e6c tests: Add the tests for the fedimg.utils
  https://github.com/fedora-infra/fedimg/commit/1788e9e6c
- ed5ddf5bf tests: Add a few more tests for utils. utils cov at 78%
  https://github.com/fedora-infra/fedimg/commit/ed5ddf5bf
- 57d4414c0 tests: Add tests for fedimg.utils, coverage 100%
  https://github.com/fedora-infra/fedimg/commit/57d4414c0
- 5ccc75652 scripts: Remove redundant imports in the trigger_upload script
  https://github.com/fedora-infra/fedimg/commit/5ccc75652
- 84cf48443 docs: Update the README.md for the trigger upload script
  https://github.com/fedora-infra/fedimg/commit/84cf48443
- 93e2358fc tests: Fix the copyright years in the test files
  https://github.com/fedora-infra/fedimg/commit/93e2358fc
- 0bcb54661 tests: Use assertIs method to check for boolean
  https://github.com/fedora-infra/fedimg/commit/0bcb54661
- b6b651f8a tests: Remove the redundant code
  https://github.com/fedora-infra/fedimg/commit/b6b651f8a
- 57a2eec93 tests: Make a stronger assertion if the urls is made to atomic and cloud base
  https://github.com/fedora-infra/fedimg/commit/57a2eec93
- 9b77f95f9 tests: Change the assertions to use self.assertIs
  https://github.com/fedora-infra/fedimg/commit/9b77f95f9
- 0f3056847 tests: include 'vcr' dependency in setup.py
  https://github.com/fedora-infra/fedimg/commit/0f3056847
- 1f29c9389 setup.py: specify test suite to use
  https://github.com/fedora-infra/fedimg/commit/1f29c9389
- 9c29204c1 setup.py: use consistent quoting for dependencies
  https://github.com/fedora-infra/fedimg/commit/9c29204c1
- 326ab9ef8 setup.py: add 'toml' dependency
  https://github.com/fedora-infra/fedimg/commit/326ab9ef8
- b206d76da setup.py: add 'fedfind' dependency
  https://github.com/fedora-infra/fedimg/commit/b206d76da
- 32533b038 tests: don't validate signatures for mockhub
  https://github.com/fedora-infra/fedimg/commit/32533b038
- 4dc97ac3f tests: add travis.yml
  https://github.com/fedora-infra/fedimg/commit/4dc97ac3f
- 5adef1a75 docs/devel: update test running instructions
  https://github.com/fedora-infra/fedimg/commit/5adef1a75
- 87f470edb fedimg.ec2: Add metadata to the `image.copy` fedmsg message
  https://github.com/fedora-infra/fedimg/commit/87f470edb
- 0ddfd41e9 fedimg.ec2: Add the support for Elastic Network Adapter
  https://github.com/fedora-infra/fedimg/commit/0ddfd41e9
- 44ac7b8b3 services.ec2: Change the bucket name to more related to fedimg
  https://github.com/fedora-infra/fedimg/commit/44ac7b8b3
- e5df4686f Error out if starting the task failed
  https://github.com/fedora-infra/fedimg/commit/e5df4686f
- 744b729ce services.ec2: Deprecate the PV images
  https://github.com/fedora-infra/fedimg/commit/744b729ce
- e1607cb5a uploader: Set push_notifications to True when automatic upload
  https://github.com/fedora-infra/fedimg/commit/e1607cb5a
- 82b63d886 fedimg: Fix the trigger_upload script to include push_notifications arg
  https://github.com/fedora-infra/fedimg/commit/82b63d886
- 0f8d6c08f readme: Update the trigger_upload usage in README file
  https://github.com/fedora-infra/fedimg/commit/0f8d6c08f
- 0dc560f13 scripts: Make the -p arg optional
  https://github.com/fedora-infra/fedimg/commit/0dc560f13
- 43103f59b scripts: Move logic inside the main function
  https://github.com/fedora-infra/fedimg/commit/43103f59b

1.0.1
-----

Pull Requests

- (@sayanchowdhury) #65, Fix the invalid syntax issue
  https://github.com/fedora-infra/fedimg/pull/65

Commits

- 8f0a92d4d utils: Fix the invalid syntax issue
  https://github.com/fedora-infra/fedimg/commit/8f0a92d4d

1.0.0
-----

Pull Requests

- (@sayanchowdhury) #61, fedimg: Migrate the CHANGELOG to rst from markdown
  https://github.com/fedora-infra/fedimg/pull/61
- (@sayanchowdhury) #62, Break fedimg into multiple components so that it is easier to maintain the AMIs
  https://github.com/fedora-infra/fedimg/pull/62

Commits

- f1d54ee2f fedimg: Migrate the CHANGELOG to rst from md
  https://github.com/fedora-infra/fedimg/commit/f1d54ee2f
- 2b7b49f8e ec2: Modularize the the structure of the ec2
  https://github.com/fedora-infra/fedimg/commit/2b7b49f8e
- a52001442 ec2: Write a publisher that would make the images & the snapshot public
  https://github.com/fedora-infra/fedimg/commit/a52001442
- ebda1518f ec2: Add a few methods to manage the AMI/Snapshots.
  https://github.com/fedora-infra/fedimg/commit/ebda1518f
- 8a5fa90e3 ec2: Remove the code from the __init__.py file.
  https://github.com/fedora-infra/fedimg/commit/8a5fa90e3
- 542ff1239 consumers: Add three different consumers for prod, stg & dev
  https://github.com/fedora-infra/fedimg/commit/542ff1239
- c794d79fe config: Migrate to mange the configuration using toml
  https://github.com/fedora-infra/fedimg/commit/c794d79fe
- 6852eb6c2 tests: Start fixing the tests using pytest
  https://github.com/fedora-infra/fedimg/commit/6852eb6c2
- 897e55db3 tests: Fix the tests for fedimg.util
  https://github.com/fedora-infra/fedimg/commit/897e55db3
- 952845601 fedimg: Modify setup according to dev, prod, and staging consumers
  https://github.com/fedora-infra/fedimg/commit/952845601
- 13d13ee6a ec2: Create a script to initiate the complete process
  https://github.com/fedora-infra/fedimg/commit/13d13ee6a
- b0b356966 ec2: Move util to utils, and fix the imports
  https://github.com/fedora-infra/fedimg/commit/b0b356966
- 4a081a7b6 consumer: Implement the util methods (they raise NotImplementError now)
  https://github.com/fedora-infra/fedimg/commit/4a081a7b6
- dbf341266 tests: Fix the test cases for the consumer
  https://github.com/fedora-infra/fedimg/commit/dbf341266
- ea14ae1ef fedimg: Add logging statements to the source
  https://github.com/fedora-infra/fedimg/commit/ea14ae1ef
- 829bfbc70 fedimg: Fix the config parsing for the general configurations
  https://github.com/fedora-infra/fedimg/commit/829bfbc70
- ad2c85df6 utils: Implement the methods `external_run_command` & `get_source_from_image`
  https://github.com/fedora-infra/fedimg/commit/ad2c85df6
- a54150605 services.ec2: Add methods to publish and copy the images to other regions
  https://github.com/fedora-infra/fedimg/commit/a54150605
- b1edcbb84 services.ec2: Update ec2initiate with the publisher code
  https://github.com/fedora-infra/fedimg/commit/b1edcbb84
- a1cf41b0d serices.ec2: Add a push_notifications flag to control msg bus push
  https://github.com/fedora-infra/fedimg/commit/a1cf41b0d
- 7283f2e2c services.ec2: Update the publisher to send messages to fedmsg
  https://github.com/fedora-infra/fedimg/commit/7283f2e2c
- f05c59c26 consumers: Add documentation to FedimgConsumer
  https://github.com/fedora-infra/fedimg/commit/f05c59c26
- 6050d2cf4 uploader: Add documentation to the fedimg uploader
  https://github.com/fedora-infra/fedimg/commit/6050d2cf4
- 9d885c461 services.ec2: Change the initiate to just handle upload of the images
  https://github.com/fedora-infra/fedimg/commit/9d885c461
- 580759f29 services.ec2: Fix the sample config file
  https://github.com/fedora-infra/fedimg/commit/580759f29
- 150a475c5 services.ec2: Create a utility method to create get the image_name
  https://github.com/fedora-infra/fedimg/commit/150a475c5
- fff538fe6 uploader: Fix the BASE_REGION in the uploader method
  https://github.com/fedora-infra/fedimg/commit/fff538fe6
- d5acfe690 services.ec2: Fix the downloading and uploading of the source
  https://github.com/fedora-infra/fedimg/commit/d5acfe690
- 84826fa57 messenger: Change the name of the method that pushes fedmsg messages
  https://github.com/fedora-infra/fedimg/commit/84826fa57
- c0cab6176 services.ec2: Fix the issues with the EC2ImgUploader
  https://github.com/fedora-infra/fedimg/commit/c0cab6176
- 600cc7c7b services.ec2: Fix the issues in the EC2ImagePublisher
  https://github.com/fedora-infra/fedimg/commit/600cc7c7b
- 9b37e0dd9 services.ec2: Attach EC2 copy to other regions into uploader
  https://github.com/fedora-infra/fedimg/commit/9b37e0dd9
- 211787e6f services.ec2: Add documentation for EC2ImgUploader
  https://github.com/fedora-infra/fedimg/commit/211787e6f
- dfd752a3c services.ec2: Change the return data from published images
  https://github.com/fedora-infra/fedimg/commit/dfd752a3c
- 9f3eb7dfd services.ec2: Fix the ec2 image publisher
  https://github.com/fedora-infra/fedimg/commit/9f3eb7dfd
- cd6a85fdb services.ec2: Change the bucket name according to Amazon S3 guidelines
  https://github.com/fedora-infra/fedimg/commit/cd6a85fdb
- d56d74447 services.ec2: Delete the resources when failed or completed
  https://github.com/fedora-infra/fedimg/commit/d56d74447
- 71cd44d05 services.ec2: Add the retry logic to fetch the snapshot details
  https://github.com/fedora-infra/fedimg/commit/71cd44d05
- 0b826f42a config: Change the config to multiple lines
  https://github.com/fedora-infra/fedimg/commit/0b826f42a
- 952500c8f fedimg: Replace the logger name to __name__
  https://github.com/fedora-infra/fedimg/commit/952500c8f
- 38f53f878 services.ec2: Fix the utility methods
  https://github.com/fedora-infra/fedimg/commit/38f53f878
- e42754240 services.ec2: Return empty if the download fails
  https://github.com/fedora-infra/fedimg/commit/e42754240
- 1df64ecc6 utils: @pypingou suggested to simplify the lambda statement
  https://github.com/fedora-infra/fedimg/commit/1df64ecc6
- f39c64a23 utils: Add the shell=True params for the shell params
  https://github.com/fedora-infra/fedimg/commit/f39c64a23
- db17bb599 config: Move the config in a single configuration file
  https://github.com/fedora-infra/fedimg/commit/db17bb599
- 6855d49ae tests: Remove the code related to vcr
  https://github.com/fedora-infra/fedimg/commit/6855d49ae

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

