Configuration
=============

Fedimg pulls its configuration variables from the file located at
`/etc/fedimg/fedimg-conf.toml`. A example file is included in the source of
fedimg, and can be used as a starting point for writing your own configuration
file.

---------------
General options
---------------

.. _conf-clean_up_on_failure:

clean_up_on_failure
-------------------
A boolean that, if ``True``, will destroy all the resources that was created,
if there is an exception during the upload process.

.. _conf-delete_image_on_failure:

delete_image_on_failure
-----------------------

A boolean that, if ``False``, will skip the the destruction of the
uploaded image if there is an exception in the upload process.

.. _conf-process_count:

process_count
-------------

An integer to specify the number of `worker process`_ that would be running.

.. _conf-active_services:

active_services
---------------

A list of active third party services where Fedimg would upload the cloud
images. Valid values within the list: `aws`.

-----------
AWS options
-----------

.. _conf-access_id:

access_id
---------

Access ID of the AWS account that will be used.

.. _conf-secret-key:

secret_key
----------

Secret Key of the AWS account that will be used.

.. _conf-base-region:

base_region
-----------

The base region among the list of AWS regions where the upload process of the
cloud images will be done.

.. _conf-bucket-name:

bucket_name
-----------

A string that contains the name of the S3 bucket used in AWS. Fedimg does not
create the S3 bucket so make sure that the bucket already exists before using.

.. _conf-regions:

regions
-------

A list containing the list of regions where the AMIs would be copied from the
``base_region``. This regions should not contain the ``base_region`` to avoid
duplicate images.

.. _conf-volume-size:

volume_size
-----------

An integer, specifying the size of the volume to be created in GiB.

.. _worker process: https://docs.python.org/2/library/multiprocessing.html#using-a-pool-of-workers
