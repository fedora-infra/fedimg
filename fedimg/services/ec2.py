# This file is part of fedimg.
# Copyright (C) 2014-2015 Red Hat, Inc.
#
# fedimg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# fedimg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#           Ralph Bean <rbean@redhat.com>
#

import logging
log = logging.getLogger("fedmsg")

from time import sleep

import paramiko
from libcloud.compute.base import NodeImage
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
from libcloud.compute.providers import get_driver
from libcloud.compute.types import DeploymentException
from libcloud.compute.types import KeyPairDoesNotExistError

import fedimg
import fedimg.messenger
from fedimg.util import get_file_arch
from fedimg.util import region_to_driver, ssh_connection_works


class EC2ServiceException(Exception):
    """ Custom exception for EC2Service. """
    pass


class EC2UtilityException(EC2ServiceException):
    """ Something went wrong with writing the image file to a volume with the
        utility instance. """
    pass


class EC2AMITestException(EC2ServiceException):
    """ Something went wrong when a newly-registered AMI was tested. """
    pass


class EC2Service(object):
    """ An object for interacting with an EC2 upload process.
        Takes a URL to a raw.xz image. """

    def __init__(self, raw_url, virt_type='hvm', vol_type='standard'):

        self.raw_url = raw_url
        self.virt_type = virt_type
        self.vol_type = vol_type
        # All of these are set to appropriate values throughout
        # the upload process.
        self.util_node = None
        self.util_volume = None
        self.images = []
        self.snapshot = None
        self.test_node = None

        self.destination = ''

        # It's possible that these values will never change
        self.test_success = False
        self.dup_count = 0  # counter: helps avoid duplicate AMI names

        # Will be lists of dicts containing AMI info
        self.util_amis = []
        self.test_amis = []

        # Populate list of AMIs by reading the AMI details from the config file
        for line in fedimg.AWS_AMIS.split('\n'):
            """ AWS_AMIS lines have pipe-delimited attrs at these indicies:
            0: region (ex. eu-west-1)
            1: OS (ex. RHEL)
            2: version (ex. 5.7)
            3: arch (ex. x86_64)
            4: ami name (ex. ami-68e3d32d) """

            # strip line to avoid any newlines or spaces from sneaking in
            attrs = line.strip().split('|')

            # old configuration
            if len(attrs)==6:

                info = {'region': attrs[0],
                        'driver': region_to_driver(attrs[0]),
                        'os': attrs[1],
                        'ver': attrs[2],
                        'arch': attrs[3],
                        'ami': attrs[4],
                        'aki': attrs[5]}

            # new configuration
            elif len(attrs)==4:

                info = {'region': attrs[0],
                        'driver': region_to_driver(attrs[0]),
                        'arch': attrs[1],
                        'ami': attrs[2],
                        'aki': attrs[3]}



            # For now, read in all AMIs to these lists, and narrow
            # down later. TODO: This could be made a bit nicer...
            self.util_amis.append(info)
            self.test_amis.append(info)

        # Get file name, build name, a description, and the image arch
        # all from the .raw.xz file name.
        self.file_name = self.raw_url.split('/')[-1]
        self.build_name = self.file_name.replace('.raw.xz', '')
        self.image_desc = "Created from build {0}".format(self.build_name)
        self.image_arch = get_file_arch(self.file_name)

        # Filter the AMI lists appropriately
        # (no EBS-enabled instance types offer a 32 bit architecture, and we
        # need EBS for registration on the utility instance, so they must be
        # x86_64)
        self.util_amis = [a for a in self.util_amis
                          if a['arch'] == 'x86_64']
        self.test_amis = [a for a in self.test_amis
                          if a['arch'] == self.image_arch]

    def _clean_up(self, driver, delete_images=False):
        """ Cleans up resources via a libcloud driver. """
        log.info('Cleaning up resources')
        if delete_images and len(self.images) > 0:
            for image in self.images:
                driver.delete_image(image)

        if self.snapshot and len(self.images) == 0:
            driver.destroy_volume_snapshot(self.snapshot)
            self.snapshot = None

        if self.util_node:
            driver.destroy_node(self.util_node)
            # Wait for node to be terminated
            while ssh_connection_works(fedimg.AWS_UTIL_USER,
                                       self.util_node.public_ips[0],
                                       fedimg.AWS_KEYPATH):
                sleep(10)
            self.util_node = None
        if self.util_volume:
            # Destroy /dev/sdb or whatever
            driver.destroy_volume(self.util_volume)
            self.util_volume = None
        if self.test_node:
            driver.destroy_node(self.test_node)
            self.test_node = None

    def upload(self, compose_meta):
        """ Registers the image in each EC2 region. """

        log.info('EC2 upload process started')

        # Get a starting utility AMI in some region to use as an origin
        ami = self.util_amis[0]  # Select the starting AMI to begin
        self.destination = 'EC2 ({region})'.format(region=ami['region'])

        fedimg.messenger.message('image.upload', self.raw_url,
                                 self.destination, 'started',
                                 compose=compose_meta)

        try:
            # Connect to the region through the appropriate libcloud driver
            cls = ami['driver']
            driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

            # select the desired node attributes
            sizes = driver.list_sizes()
            reg_size_id = 'm1.xlarge'

            # check to make sure we have access to that size node
            # TODO: Add try/except if for some reason the size isn't
            # available?
            size = [s for s in sizes if s.id == reg_size_id][0]
            base_image = NodeImage(id=ami['ami'], name=None, driver=driver)

            # Name the utility node
            name = 'Fedimg AMI builder'

            # Block device mapping for the utility node
            # (Requires this second volume to write the image to for
            # future registration.)
            mappings = [{'VirtualName': None,  # cannot specify with Ebs
                         'Ebs': {'VolumeSize': fedimg.AWS_UTIL_VOL_SIZE,
                                 'VolumeType': self.vol_type,
                                 'DeleteOnTermination': 'false'},
                         'DeviceName': '/dev/sdb'}]

            # Read in the SSH key
            with open(fedimg.AWS_PUBKEYPATH, 'rb') as f:
                key_content = f.read()

            # Add key to authorized keys for root user
            step_1 = SSHKeyDeployment(key_content)

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"  # this isn't so important for the util inst.
            step_2 = ScriptDeployment(script)

            # Create deployment object (will set up SSH key and run script)
            msd = MultiStepDeployment([step_1, step_2])

            log.info('Deploying utility instance')
            while True:
                try:
                    self.util_node = driver.deploy_node(
                        name=name,
                        image=base_image,
                        size=size,
                        ssh_username=fedimg.AWS_UTIL_USER,
                        ssh_alternate_usernames=[''],
                        ssh_key=fedimg.AWS_KEYPATH,
                        deploy=msd,
                        kernel_id=ami['aki'],
                        ex_metadata={'build':
                                     self.build_name},
                        ex_keyname=fedimg.AWS_KEYNAME,
                        ex_security_groups=['ssh'],
                        ex_ebs_optimized=True,
                        ex_blockdevicemappings=mappings)

                except KeyPairDoesNotExistError:
                    # The keypair is missing from the current region.
                    # Let's install it and try again.
                    log.exception('Adding missing keypair to region')
                    driver.ex_import_keypair(fedimg.AWS_KEYNAME,
                                             fedimg.AWS_PUBKEYPATH)
                    continue

                except Exception as e:
                    # We might have an invalid security group, aka the 'ssh'
                    # security group doesn't exist in the current region. The
                    # reason this is caught here is because the related
                    # exception that prints`InvalidGroup.NotFound is, for
                    # some reason, a base exception.
                    if 'InvalidGroup.NotFound' in str(e):
                        log.exception('Adding missing security'
                                      'group to region')
                        # Create the ssh security group
                        driver.ex_create_security_group('ssh', 'ssh only')
                        driver.ex_authorize_security_group('ssh', '22', '22',
                                                           '0.0.0.0/0')
                        continue
                    else:
                        raise
                break

            # Wait until the utility node has SSH running
            while not ssh_connection_works(fedimg.AWS_UTIL_USER,
                                           self.util_node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                sleep(10)

            log.info('Utility node started with SSH running')

            # Connect to the utility node via SSH
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.util_node.public_ips[0],
                           username=fedimg.AWS_UTIL_USER,
                           key_filename=fedimg.AWS_KEYPATH)

            # Curl the .raw.xz file down from the web, decompressing it
            # and writing it to the secondary volume defined earlier by
            # the block device mapping.
            # curl with -L option, so we follow redirects
            cmd = "sudo sh -c 'curl -L {0} | xzcat > /dev/xvdb'".format(
                  self.raw_url)
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around require tty

            log.info('Executing utility script')

            # Run the above command and wait for its exit status
            chan.exec_command(cmd)
            status = chan.recv_exit_status()
            if status != 0:
                # There was a problem with the SSH command
                log.error('Problem writing volume with utility instance')

                data = "(no data)"
                if chan.recv_ready():
                    data = chan.recv(1024 * 32)

                fedimg.messenger.message('image.upload', self.raw_url,
                                         self.destination, 'failed',
                                         extra={'data': data},
                                         compose=compose_meta)

                raise EC2UtilityException(
                    "Problem writing image to utility instance volume. "
                    "Command exited with status {0}.\n"
                    "command: {1}\n"
                    "output: {2}".format(status, cmd, data))

            client.close()

            # Get volume name that image was written to
            vol_id = [x['ebs']['volume_id'] for x in
                      self.util_node.extra['block_device_mapping'] if
                      x['device_name'] == '/dev/sdb'][0]

            log.info('Destroying utility node')

            # Terminate the utility instance
            driver.destroy_node(self.util_node)

            # Wait for utility node to be terminated
            while ssh_connection_works(fedimg.AWS_UTIL_USER,
                                       self.util_node.public_ips[0],
                                       fedimg.AWS_KEYPATH):
                sleep(10)

            # Wait a little longer since loss of SSH connectivity doesn't mean
            # that the node's destroyed
            # TODO: Check instance state rather than this lame sleep thing
            sleep(45)

            # Take a snapshot of the volume the image was written to
            self.util_volume = [v for v in driver.list_volumes()
                                if v.id == vol_id][0]
            snap_name = 'fedimg-snap-{0}'.format(self.build_name)

            log.info('Taking a snapshot of the written volume')

            self.snapshot = driver.create_volume_snapshot(self.util_volume,
                                                          name=snap_name)
            snap_id = str(self.snapshot.id)

            while self.snapshot.extra['state'] != 'completed':
                # Re-obtain snapshot object to get updates on its state
                self.snapshot = [s for s in driver.list_snapshots()
                                 if s.id == snap_id][0]
                sleep(10)

            # Make the snapshot public, so that the AMIs can be copied
            is_snapshot_public = False
            while True:
                is_snapshot_public = driver.ex_modify_snapshot_attribute(self.snapshot, {
                    'CreateVolumePermission.Add.1.Group': 'all'
                })
                if is_snapshot_public:
                    break

                log.info('Snapshot is not public yet. Retry in 20')
                sleep(20)

            log.info('Snapshot taken & made public')

            # Delete the volume now that we've got the snapshot
            driver.destroy_volume(self.util_volume)
            # make sure Fedimg knows that the vol is gone
            self.util_volume = None

            log.info('Destroyed volume')

            # Actually register image
            log.info('Registering image as an AMI')

            if self.virt_type == 'paravirtual':
                image_name = "{0}-{1}-PV-{2}-0".format(self.build_name,
                                                  ami['region'],
                                                  self.vol_type)
                test_size_id = 'm1.xlarge'
                # test_amis will include AKIs of the appropriate arch
                registration_aki = [a['aki'] for a in self.test_amis
                                    if a['region'] == ami['region']][0]
                reg_root_device_name = '/dev/sda'
            else:  # HVM
                image_name = "{0}-{1}-HVM-{2}-0".format(self.build_name,
                                                    ami['region'],
                                                    self.vol_type)
                test_size_id = 'm3.2xlarge'
                # Can't supply a kernel image with HVM
                registration_aki = None
                reg_root_device_name = '/dev/sda1'

            # For this block device mapping, we have our volume be
            # based on the snapshot's ID
            mapping = [{'DeviceName': reg_root_device_name,
                        'Ebs': {'SnapshotId': snap_id,
                                'VolumeSize': fedimg.AWS_TEST_VOL_SIZE,
                                'VolumeType': self.vol_type,
                                'DeleteOnTermination': 'true'}}]

            # Avoid duplicate image name by incrementing the number at the
            # end of the image name if there is already an AMI with that name.
            # TODO: This process could be written nicer.
            while True:
                try:
                    if self.dup_count > 0:
                        # Remove trailing '-0' or '-1' or '-2' or...
                        image_name = '-'.join(image_name.split('-')[:-1])
                        # Re-add trailing dup number with new count
                        image_name += '-{0}'.format(self.dup_count)
                    # Try to register with that name
                    self.images.append(driver.ex_register_image(
                        image_name,
                        description=self.image_desc,
                        root_device_name=reg_root_device_name,
                        block_device_mapping=mapping,
                        virtualization_type=self.virt_type,
                        kernel_id=registration_aki,
                        architecture=self.image_arch))
                except Exception as e:
                    # Check if the problem was a duplicate name
                    if 'InvalidAMIName.Duplicate' in str(e):
                        # Keep trying until an unused name is found
                        self.dup_count += 1
                        continue
                    else:
                        raise
                break

            log.info('Completed image registration')

            # Emit success fedmsg
            # TODO: Can probably move this into the above try/except,
            # to avoid just dumping all the messages at once.
            for image in self.images:
                fedimg.messenger.message('image.upload', self.raw_url,
                                         self.destination, 'completed',
                                         extra={'id': image.id,
                                                'virt_type': self.virt_type,
                                                'vol_type': self.vol_type},
                                         compose=compose_meta)

            # Now, we'll spin up a node of the AMI to test:

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            log.info('Deploying test node')

            # Pick a name for the test instance
            name = 'Fedimg AMI tester'

            # Select the appropriate size for the instance
            size = [s for s in sizes if s.id == test_size_id][0]

            # Alert the fedmsg bus that an image test is starting
            fedimg.messenger.message('image.test', self.raw_url,
                                     self.destination, 'started',
                                     extra={'id': self.images[0].id,
                                            'virt_type': self.virt_type,
                                            'vol_type': self.vol_type},
                                     compose=compose_meta)

            # Actually deploy the test instance
            try:
                self.test_node = driver.deploy_node(
                    name=name, image=self.images[0], size=size,
                    ssh_username=fedimg.AWS_TEST_USER,
                    ssh_alternate_usernames=['root'],
                    ssh_key=fedimg.AWS_KEYPATH,
                    deploy=msd,
                    kernel_id=registration_aki,
                    ex_metadata={'build': self.build_name},
                    ex_keyname=fedimg.AWS_KEYNAME,
                    ex_security_groups=['ssh'],
                    )
            except Exception as e:
                fedimg.messenger.message('image.test', self.raw_url,
                                         self.destination, 'failed',
                                         extra={'id': self.images[0].id,
                                                'virt_type': self.virt_type,
                                                'vol_type': self.vol_type},
                                         compose=compose_meta)

                raise EC2AMITestException("Failed to boot test node %r." % e)

            # Wait until the test node has SSH running
            while not ssh_connection_works(fedimg.AWS_TEST_USER,
                                           self.test_node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                sleep(10)

            log.info('Starting AMI tests')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.test_node.public_ips[0],
                           username=fedimg.AWS_TEST_USER,
                           key_filename=fedimg.AWS_KEYPATH)

            # Run /bin/true on the test instance as a simple "does it
            # work" test
            cmd = "/bin/true"
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around requiretty

            log.info('Running AMI test script')

            chan.exec_command(cmd)

            # Again, wait for the test command's exit status
            if chan.recv_exit_status() != 0:
                # There was a problem with the SSH command
                log.error('Problem testing new AMI')

                data = "(no data)"
                if chan.recv_ready():
                    data = chan.recv(1024 * 32)

                fedimg.messenger.message('image.test', self.raw_url,
                                         self.destination, 'failed',
                                         extra={'id': self.images[0].id,
                                                'virt_type': self.virt_type,
                                                'vol_type': self.vol_type,
                                                'data': data},
                                         compose=compose_meta)

                raise EC2AMITestException("Tests on AMI failed.\n"
                                          "output: %s" % data)

            client.close()

            log.info('AMI test completed')
            fedimg.messenger.message('image.test', self.raw_url,
                                     self.destination, 'completed',
                                     extra={'id': self.images[0].id,
                                            'virt_type': self.virt_type,
                                            'vol_type': self.vol_type},
                                     compose=compose_meta)

            # Let this EC2Service know that the AMI test passed, so
            # it knows how to proceed.
            self.test_success = True

            log.info('Destroying test node')

            # Destroy the test node
            driver.destroy_node(self.test_node)

            # Make AMIs public
            for image in self.images:
                driver.ex_modify_image_attribute(
                    image,
                    {'LaunchPermission.Add.1.Group': 'all'})

        except EC2UtilityException as e:
            log.exception("Failure")
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_images=fedimg.DELETE_IMAGES_ON_FAILURE)
            return 1

        except EC2AMITestException as e:
            log.exception("Failure")
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_images=fedimg.DELETE_IMAGES_ON_FAILURE)
            return 1

        except DeploymentException as e:
            log.exception("Problem deploying node: {0}".format(e.value))
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_images=fedimg.DELETE_IMAGES_ON_FAILURE)
            return 1

        except Exception as e:
            # Just give a general failure message.
            log.exception("Unexpected exception")
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_images=fedimg.DELETE_IMAGES_ON_FAILURE)
            return 1

        else:
            self._clean_up(driver)

        if self.test_success:
            # Copy the AMI to every other region if tests passed
            copied_images = list()  # completed image copies (ami: image)

            # Use the AMI list as a way to cycle through the regions
            for ami in self.test_amis[1:]:  # we don't need the origin region

                # Choose an appropriate destination name for the copy
                alt_dest = 'EC2 ({region})'.format(
                    region=ami['region'])

                fedimg.messenger.message('image.upload',
                                         self.raw_url,
                                         alt_dest, 'started',
                                         compose=compose_meta)

                # Connect to the libcloud EC2 driver for the region we
                # want to copy into
                alt_cls = ami['driver']
                alt_driver = alt_cls(fedimg.AWS_ACCESS_ID,
                                     fedimg.AWS_SECRET_KEY)

                # Construct the full name for the image copy
                if self.virt_type == 'paravirtual':
                    image_name = "{0}-{1}-PV-{2}-0".format(
                        self.build_name, ami['region'], self.vol_type)
                else:  # HVM
                    image_name = "{0}-{1}-HVM-{2}-0".format(
                        self.build_name, ami['region'], self.vol_type)

                log.info('AMI copy to {0} started'.format(ami['region']))

                # Avoid duplicate image name by incrementing the number at the
                # end of the image name if there is already an AMI with
                # that name.
                # TODO: Again, this could be written better
                while True:
                    try:
                        if self.dup_count > 0:
                            # Remove trailing '-0' or '-1' or '-2' or...
                            image_name = '-'.join(image_name.split('-')[:-1])
                            # Re-add trailing dup number with new count
                            image_name += '-{0}'.format(self.dup_count)

                        # Actually run the image copy from the origin region
                        # to the current region.
                        for image in self.images:
                            image_copy = alt_driver.copy_image(
                                image,
                                self.test_amis[0]['region'],
                                name=image_name,
                                description=self.image_desc)
                            # Add the image copy to a list so we can work with
                            # it later.
                            copied_images.append(image_copy)

                            log.info('AMI {0} copied to AMI {1}'.format(
                                image, image_name))

                    except Exception as e:
                        # Check if the problem was a duplicate name
                        if 'InvalidAMIName.Duplicate' in str(e):
                            # Keep trying until an unused name is found.
                            # This probably won't trigger, since it seems
                            # like EC2 doesn't mind duplicate AMI names
                            # when they are being copied, only registered.
                            # Strange, but apprently true.
                            self.dup_count += 1
                            continue
                        else:
                            # TODO: Catch a more specific exception
                            log.exception(
                                'Image copy to {0} failed'.format(
                                    ami['region']))
                            fedimg.messenger.message('image.upload',
                                                     self.raw_url,
                                                     alt_dest, 'failed',
                                                     compose=compose_meta)
                    break

            # Now cycle through and make all of the copied AMIs public
            # once the copy process has completed. Again, use the test
            # AMI list as a way to have region and arch data:

            # We don't need the origin region, since the AMI was made there:
            self.test_amis = self.test_amis[1:]

            for image in copied_images:
                ami = self.test_amis[copied_images.index(image)]
                alt_cls = ami['driver']
                alt_driver = alt_cls(fedimg.AWS_ACCESS_ID,
                                     fedimg.AWS_SECRET_KEY)

                # Get an appropriate name for the region in question
                alt_dest = 'EC2 ({region})'.format(region=ami['region'])

                # Need to wait until the copy finishes in order to make
                # the AMI public.
                is_image_public = False
                while True:
                    try:
                        # Make the image public
                        is_image_public = alt_driver.ex_modify_image_attribute(
                            image,
                            {'LaunchPermission.Add.1.Group': 'all'}
                        )
                    except Exception as e:
                        if 'InvalidAMIID.Unavailable' in str(e):
                            # The copy isn't done, so wait 20 seconds
                            # and try again.
                            sleep(20)
                            continue
                    break

                if is_image_public:
                    log.info('Made {0} public ({1}, {2}, {3}, {4})'.format(
                        image.id, self.build_name, self.virt_type,
                        self.vol_type, ami['region']))
                else:
                    log.info('{0} is private ({1}, {2}, {3}, {4})'.format(
                        image.id, self.build_name, self.virt_type,
                        self.vol_type, ami['region']))

                # Make the snapshot for the image public.
                is_snapshot_public = False
                snapshot = None

                alt_ami = alt_driver.get_image(image.id)
                blk_device_mapping = alt_ami.extra['block_device_mapping']
                if len(blk_device_mapping) == 1:
                    snapshot_id = blk_device_mapping[0]['ebs']['snapshot_id']

                    # The `list_snapshots` method requires a snapshot object.
                    # which then fetches the id of the snapshot and fetches the
                    # detail of the snapshot. So, I am making an empty snapshot
                    # object here and attaching the value to the `id` attribute
                    # so that the list_snapshots method just works
                    snapshot_obj = type('', (), {})()
                    snapshot_obj.id = snapshot_id
                    snapshot = alt_driver.list_snapshots(snapshot=snapshot_obj)

                if snapshot is not None:
                    snapshot = snapshot[0]
                    while True:
                        is_snapshot_public = (
                            alt_driver.ex_modify_snapshot_attribute(
                                snapshot, {
                                    'CreateVolumePermission.Add.1.Group': 'all'
                                })
                            )
                        if is_snapshot_public:
                            break

                        log.info('Snapshot is not public yet. Retry in 20')
                        sleep(20)
                else:
                    is_snapshot_public = False
                    log.info('Search (%s, %s) returned no results' % (
                        snapshot_id, ami['region']))

                if is_snapshot_public:
                    log.info('Snapshot (%s, %s) made public' % (
                        snapshot_id, ami['region']))
                else:
                    log.info('Snapshot (%s, %s) still private' % (
                        snapshot_id, ami['region']))

                fedimg.messenger.message('image.upload',
                                         self.raw_url,
                                         alt_dest, 'completed',
                                         extra={'id': image.id,
                                                'virt_type': self.virt_type,
                                                'vol_type': self.vol_type},
                                         compose=compose_meta)

            return 0
