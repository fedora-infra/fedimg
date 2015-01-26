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

## Custom exceptions

The EC2 service defines three custom exceptions that can be raised by the service.

-   `EC2ServiceException`, a generic exception (inherits from `Exception`).
-   `EC2UtilityException`, which can arise when there is a problem with the
    utility instance (inherits from `EC2ServiceException`).
-   `EC2TestException`, which can arise when there is an issue with the test
    instance (inherits from `EC2ServiceException`).
