Fedimg is hooked into Amazon Web Services and registers images as public AMIs in all
EC2 regions. This page explains the process, which takes place in
`fedimg/services/ec2.py`.

## AMI types

At the time of this writing, it seems that we'll eventually want to provide
potentially six different AMIs for each Fedora Cloud image processed.

<table>
<tr><th>Virtualization</th><th>Storage</th><th>Result</th></tr>
<tr><td>Paravirtual</td><td>Instance-Store</td><td>1 bundle * </td></tr>
<tr><td>Paravirtual</td><td>EBS</td><td>1 snapshot, 2 volume types</td></tr>
<tr><td>Paravirtual</td><td>EBS (encrypted)</td><td>1 snapshot, 2 volume types * </td></tr>
<tr><td>HVM</td><td>Instance-Store</td><td>1 bundle * </td></tr>
<tr><td>HVM</td><td>EBS</td><td>1 snapshot, 2 volume types</td></tr>
<tr><td>HVM</td><td>EBS (encrypted)</td><td>1 snapshot, 2 volume types * </td></tr>
</table>
`*`: Not yet added to Fedimg

*The "2 volume types" mentioned in this table are Standard and GP2. GP2 is a new
SSD-based type Amazon is encouraging. It has different pricing and performance
characteristics.*

## Terminology

An **instance** is a virtual machine that exists on EC2. They are started from
an AMI. To put it simply, an instance is a computer.

An **AMI**, or **Amazon Machine Image**, is essentially a picture of a
potential instance. The AMI defines everything about how the new instance will
be, including the operating system and all files that the system will be born
with. It is what is used to start a new instance on EC2. Fedimg registers
Fedora images as public AMIs so they are freely available in all regions for
testing and use.

The **utility instance** is the instance which downloads the raw image file and
writes it to a volume for snapshotting. It is the first instance that is
launched during the EC2 service.

The **test instance** is launched from an AMI that Fedimg has registered.
Fedimg can be easily configured to perform tests on this instance to
determine the health of the new AMI. It is the second instance that is created
during the EC2 service.

## Process

When the uploader calls on the EC2 service, the following happens:

1.  The AWS AMI list in `/etc/fedimg.cfg` is read in.

2.  A utility instance is deployed using the properties from the first item
    in the AMI list.

3.  The utility instance uses `curl` to pull down the `.raw.xz` image file
    and writes it to a blank volume. This volume is then snapshotted and
    subsequently destroyed.

4.  The volume snapshot is used to register the image as an AMI. Images
    are registered with both standard and GP2 volume types, as well as
    with both paravirtual and HVM virtualization.

5.  The utility instance is shut down, and a test instance is started,
    using the AMI that was just registered.

6.  The test script (configured in `/etc/fedimg.cfg`) is executed on the
    test node. If it exits with status code 0, the tests are considered
    to have passed. (In the future, [Tunir](http://tunir.readthedocs.org/en/latest/)
    will be used for testing.)

7.  If the tests passed, the AMI is copied to all other EC2 regions.

8.  All AMIs are made public.

Fedmsgs are emitted throughout this process, notifying when an image upload
or test is started, completed, or fails.

## Getting AMI info

The EC2 service produces publicly-available AMIs in a variety of flavors.
You can get the IDs and other information about these AMIs in a few different
ways:

1.  The preferred way at the moment is to just check Datagrepper. You can
    see the results of the latest image uploads by visiting a URL like
    [this](https://apps.fedoraproject.org/datagrepper/raw/?topic=org.fedoraproject.prod.fedimg.image.upload).
    Just click "Details" for any of the completed upload jobs, and you can
    see the AMI ID, as well as other info.

2.  AMI info is displayed on the [releng dashboard](https://apps.fedoraproject.org/releng-dash/),
    though it's not quite complete yet. It only displays the very latest
    upload jobs, and only a few of them at a time. The releng dash is currently
    undergoing a rewrite, and this option for getting AMI info will be much
    more useful in the future.

3.  If you have access to the machine that Fedimg is running on, or if you've
    triggered a manual upload job, Fedimg outputs AMI info to stdout as well
    as in the logs, which can be accessed with `journalctl`. Fedimg logging
    goes through fedmsg-hub, so you could check these logs with a command
    like `journalctl -u fedmsg-hub`.

## Custom exceptions

The EC2 service defines three custom exceptions that can be raised by the service.

-   `EC2ServiceException`, a generic exception (inherits from `Exception`).
-   `EC2UtilityException`, which can arise when there is a problem with the
    utility instance (inherits from `EC2ServiceException`).
-   `EC2TestException`, which can arise when there is an issue with the test
    instance (inherits from `EC2ServiceException`).
