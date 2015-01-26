Fedimg pulls its configuration variables from the file located at
`/etc/fedimg.cfg`. The file `fedimg.cfg.example` included with Fedimg can be
used as a starting point for writing your own configuration file.

At the time of this writing, the configuration file is read in when Fedimg is
initialized, so it may be necessary to restart Fedimg after making a
configuration change.

## General options

`clean_up_on_failure` can be set to `False` in order to skip the destruction of
instances, volumes, and other resources if there is an exception in the upload
process.

`delete_image_on_failure` can be set to `False` to skip the destruction of the
uploaded image if there is an exception in the upload process.

## Koji options

`server` is the URL of the Koji server.

`base_task_url` is the tasks URL that Fedimg will use to prefix the specific
task address. Example: `https://kojipkgs.fedoraproject.org//work/tasks`

## AWS options

`util_username` is the username that will be used to SSH into the utility
instance. It should be an account that already exists in the AMI.

`test_username` is the username that will be used to SSH into the test
instance launched from the newly registered AMI. The test script will
be executed by this account.

`util_volume_size` is the size, in GB, that will be used for
the volume that the utility instance writes the image to.

`test_volume_size` is the size, in GB, that the AMI will be registered
with. It will likely be the same as `util_volume_size`.

`access_id` is the access ID for the AWS account that will be used.

`secret_key` is the secret key of the AWS account that will be used.

`iam_profile` is the name of the IAM profile that will be used. **This is
currently unused.**

`keyname` is the name of the keypair that will be used.

`keypath` is the path to the private key that will be used.

`pubkeypath` is the path to the public key that will be used.

`test` is the test script that should be run on the test instance.

`amis` is a list of AMIs that Fedimg can use to start utility instances. There
should be 16 entries, one for i386 and one for x86_64 in each region. See
`fedimg.cfg.example` for example entries.They are formatted as follows:

```
<region>|<os>|<version>|<architecture>|<ami_id>|<aki_id>
```

## Rackspace options

**These are currently unused.**

## GCE options

**These are currently unused.**

## HP options

**These are currently unused.**
