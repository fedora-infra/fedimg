# This file is part of fedimg.
# Copyright (C) 2014 Red Hat, Inc.
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
#

import logging
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
from fedimg.util import get_file_arch, get_virt_type, ssh_connection_works
from fedimg.util import region_to_provider


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
    """ A class for interacting with an EC2 connection. """

    def __init__(self):
        self.util_node = None
        self.util_volume = None
        self.snapshot = None
        self.image = None
        self.image_desc = None
        self.test_node = None
        self.build_name = 'Fedimg build'
        self.destination = 'somewhere'
        self.test_success = False
        self.dup_count = 0  # counter: helps avoid duplicate AMI names
        self.amis = list()  # Will contain dicts. Dicts will contain AMI info.

        # Populate list of AMIs by reading the AMI details from the config
        # file.
        for line in fedimg.AWS_AMIS.split('\n'):
            """ AWS_AMIS lines have pipe-delimited attrs at these indicies:
            0: region (ex. eu-west-1)
            1: OS (ex. RHEL)
            2: version (ex. 5.7)
            3: arch (ex. x86_64)
            4: ami name (ex. ami-68e3d32d) """

            # strip line to avoid any newlines or spaces from sneaking in
            attrs = line.strip().split('|')

            info = {'region': attrs[0],
                    'prov': region_to_provider(attrs[0]),
                    'os': attrs[1],
                    'ver': attrs[2],
                    'arch': attrs[3],
                    'ami': attrs[4],
                    'aki': attrs[5]}
            self.amis.append(info)

    def _clean_up(self, driver, delete_image=False):
        """ Cleans up resources via a libcloud driver. """
        logging.info('Cleaning up resources')
        if delete_image and self.image:
            driver.delete_image(self.image)
            self.image = None

        if self.snapshot and not self.image:
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

    def upload(self, raw_url):
        """ Takes a URL to a .raw.xz file and registers it as an AMI in each
        EC2 region. """

        logging.info('EC2 upload process started')

        fedimg.messenger.message('image.upload', self.build_name,
                                 self.destination, 'started')

        try:
            file_name = raw_url.split('/')[-1]
            self.build_name = file_name.replace('.raw.xz', '')
            self.image_desc = "Created from build {0}".format(self.build_name)
            image_arch = get_file_arch(file_name)
            # no EBS-enabled instance types offer a 32 bit architecture
            self.amis = [a for a in self.amis if a['arch'] == 'x86_64']
            ami = self.amis[0]
            self.destination = 'EC2 ({region})'.format(region=ami['region'])

            cls = get_driver(ami['prov'])
            driver = cls(fedimg.AWS_ACCESS_ID, fedimg.AWS_SECRET_KEY)

            # select the desired node attributes
            sizes = driver.list_sizes()
            reg_size_id = 'm1.large'
            # check to make sure we have access to that size node
            size = [s for s in sizes if s.id == reg_size_id][0]
            base_image = NodeImage(id=ami['ami'], name=None, driver=driver)

            # deploy node
            name = 'Fedimg AMI builder'
            mappings = [{'VirtualName': None,  # cannot specify with Ebs
                         'Ebs': {'VolumeSize': 12,  # 12 GB should be enough
                                 'VolumeType': 'standard',
                                 'DeleteOnTermination': 'false'},
                         'DeviceName': '/dev/sdb'}]

            # read in ssh key
            with open(fedimg.AWS_PUBKEYPATH, 'rb') as f:
                key_content = f.read()

            # Add key to authorized keys for root user
            step_1 = SSHKeyDeployment(key_content)

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            logging.info('Deploying utility instance')

            # Must be EBS-backed for AMI registration to work.
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
                    # Let's install it.
                    logging.exception('Adding missing keypair to region')
                    driver.ex_import_keypair(fedimg.AWS_KEYNAME,
                                             fedimg.AWS_PUBKEYPATH)
                    continue

                except Exception as e:
                    # We might have an invalid security group, aka the 'ssh'
                    # security group doesn't exist in the current region. The
                    # reason this is caught here is because the related
                    # exception that prints `InvalidGroup.NotFound` is, for
                    # some reason, a base exception.
                    if 'InvalidGroup.NotFound' in e.message:
                        logging.exception('Adding missing security'
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

            logging.info('Utility node started with SSH running')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.util_node.public_ips[0],
                           username=fedimg.AWS_UTIL_USER,
                           key_filename=fedimg.AWS_KEYPATH)
            cmd = "sudo sh -c 'curl {0} | xzcat > /dev/xvdb'".format(raw_url)
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around requiretty

            logging.info('Executing utility script')

            chan.exec_command(cmd)
            status = chan.recv_exit_status()
            if status != 0:
                # There was a problem with the SSH command
                logging.error('Problem writing volume with utility instance')
                raise EC2UtilityException("Problem writing image to"
                                          " utility instance volume."
                                          " Command exited with"
                                          " status {0}.\n"
                                          "command: {1}".format(status, cmd))
            client.close()

            # Get volume name that image was written to
            vol_id = [x['ebs']['volume_id'] for x in
                      self.util_node.extra['block_device_mapping'] if
                      x['device_name'] == '/dev/sdb'][0]

            logging.info('Destroying utility node')

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

            logging.info('Taking a snapshot of the written volume')

            self.snapshot = driver.create_volume_snapshot(self.util_volume,
                                                          name=snap_name)
            snap_id = str(self.snapshot.id)

            while self.snapshot.extra['state'] != 'completed':
                # need to re-pull snapshot object to get updates
                self.snapshot = [s for s in driver.list_snapshots()
                                 if s.id == snap_id][0]
                sleep(10)

            logging.info('Snapshot taken')

            # Delete the volume now that we've got the snapshot
            driver.destroy_volume(self.util_volume)
            # make sure Fedimg knows that the vol is gone
            self.util_volume = None

            logging.info('Destroyed volume')

            # Actually register image
            logging.info('Registering image as an AMI')
            image_name = "{0}-{1}-0".format(self.build_name, ami['region'])

            virt_type = get_virt_type(image_name)

            if virt_type == 'paravirtual':
                test_size_id = 'm1.medium'
                registration_aki = ami['aki']
                test_aki = ami['aki']
                reg_root_device_name = '/dev/sda'
            else:  # HVM
                test_size_id = 'm3.medium'
                # Can't supply a kernel image with HVM
                registration_aki = None
                test_aki = None
                reg_root_device_name = '/dev/sda1'

            # Block device mapping for the AMI
            mapping = [{'DeviceName': reg_root_device_name,
                        'Ebs': {'SnapshotId': snap_id,
                                'VolumeSize': 12,
                                'VolumeType': 'standard',
                                'DeleteOnTermination': 'true'}}]

            # Avoid duplicate image name by incrementing the number at the
            # end of the image name if there is already an AMI with that name.
            while True:
                try:
                    if self.dup_count > 0:
                        # Remove trailing '-0' or '-1' or '-2' or...
                        image_name = '-'.join(image_name.split('-')[:-1])
                        # Re-add trailing dup number with new count
                        image_name += '-{0}'.format(self.dup_count)
                    # Try to register with that name
                    self.image = driver.ex_register_image(
                        image_name,
                        description=self.image_desc,
                        root_device_name=reg_root_device_name,
                        block_device_mapping=mapping,
                        virtualization_type=virt_type,
                        kernel_id=registration_aki,
                        architecture=image_arch)
                except Exception as e:
                    # Check if the problem was a duplicate name
                    if 'InvalidAMIName.Duplicate' in e.message:
                        # Keep trying until an unused name is found
                        self.dup_count += 1
                        continue
                    else:
                        raise
                break

            logging.info('Completed image registration')

            # Emit success fedmsg
            fedimg.messenger.message('image.upload', self.build_name,
                                     self.destination, 'completed',
                                     extra={'id': self.image.id})

            # Spin up a node of the AMI to test

            # Add script for deployment
            # Device becomes /dev/xvdb on instance
            script = "touch test"
            step_2 = ScriptDeployment(script)

            # Create deployment object
            msd = MultiStepDeployment([step_1, step_2])

            logging.info('Deploying test node')

            name = 'Fedimg AMI tester'
            size = [s for s in sizes if s.id == test_size_id][0]

            self.test_node = driver.deploy_node(
                name=name, image=self.image, size=size,
                ssh_username=fedimg.AWS_TEST_USER,
                ssh_alternate_usernames=['root'],
                ssh_key=fedimg.AWS_KEYPATH,
                deploy=msd,
                kernel_id=test_aki,
                ex_metadata={'build': self.build_name},
                ex_keyname=fedimg.AWS_KEYNAME,
                ex_security_groups=['ssh'],
                )

            # Wait until the test node has SSH running
            while not ssh_connection_works(fedimg.AWS_TEST_USER,
                                           self.test_node.public_ips[0],
                                           fedimg.AWS_KEYPATH):
                sleep(10)

            logging.info('Starting AMI tests')

            # Alert the fedmsg bus that an image test has started
            fedimg.messenger.message('image.test', self.build_name,
                                     self.destination, 'started')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.test_node.public_ips[0],
                           username=fedimg.AWS_TEST_USER,
                           key_filename=fedimg.AWS_KEYPATH)
            cmd = "true"
            chan = client.get_transport().open_session()
            chan.get_pty()  # Request a pseudo-term to get around requiretty

            logging.info('Running AMI test script')

            chan.exec_command(cmd)
            if chan.recv_exit_status() != 0:
                # There was a problem with the SSH command
                logging.error('Problem testing new AMI')
                raise EC2AMITestException("Tests on AMI failed.")

            logging.info('AMI test completed')
            fedimg.messenger.message('image.test', self.build_name,
                                     self.destination, 'completed',
                                     extra={'id': self.image.id})
            self.test_success = True

            logging.info('Destroying test node')

            # Destroy the test node
            driver.destroy_node(self.test_node)

            # Make AMI public
            driver.ex_modify_image_attribute(
                self.image,
                {'LaunchPermission.Add.1.Group': 'all'})

        except EC2UtilityException as e:
            fedimg.messenger.message('image.upload', self.build_name,
                                     self.destination, 'failed')
            print "Failure:", e
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_image=fedimg.DELETE_IMAGE_ON_FAILURE)

        except EC2AMITestException as e:
            fedimg.messenger.message('image.test', self.build_name,
                                     self.destination, 'failed')
            print "Failure:", e
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_image=fedimg.DELETE_IMAGE_ON_FAILURE)

        except DeploymentException as e:
            fedimg.messenger.message('image.upload', self.build_name,
                                     self.destination, 'failed')
            print "Problem deploying node: {0}".format(e.value)
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_image=fedimg.DELETE_IMAGE_ON_FAILURE)

        except Exception as e:
            # Just give a general failure message.
            fedimg.messenger.message('image.upload', self.build_name,
                                     self.destination, 'failed')
            print "Unexpected exception:", e
            if fedimg.CLEAN_UP_ON_FAILURE:
                self._clean_up(driver,
                               delete_image=fedimg.DELETE_IMAGE_ON_FAILURE)

        else:
            self._clean_up(driver)

        if self.test_success:
            # Copy the AMI to every other region if tests passed
            copied_images = list()  # completed image copies (ami: image)
            for ami in self.amis[1:]:

                alt_dest = 'EC2 ({region})'.format(
                    region=ami['region'])

                fedimg.messenger.message('image.upload',
                                         self.build_name,
                                         alt_dest, 'started')

                alt_cls = get_driver(ami['prov'])
                alt_driver = alt_cls(fedimg.AWS_ACCESS_ID,
                                     fedimg.AWS_SECRET_KEY)

                image_name = "{0}-{1}-0".format(
                    self.build_name, ami['region'])

                logging.info('AMI copy to {0} started'.format(
                    ami['region']))

                # Avoid duplicate image name by incrementing the number at the
                # end of the image name if there is already an AMI with
                # that name.
                while True:
                    try:
                        if self.dup_count > 0:
                            # Remove trailing '-0' or '-1' or '-2' or...
                            image_name = '-'.join(image_name.split('-')[:-1])
                            # Re-add trailing dup number with new count
                            image_name += '-{0}'.format(self.dup_count)

                        image_copy = alt_driver.copy_image(
                            self.image,
                            self.amis[0]['region'],
                            name=image_name,
                            description=self.image_desc)

                        copied_images.append(image_copy)

                        logging.info('AMI {0} copied to AMI {1}'.format(
                            self.image, image_name))
                    except Exception as e:
                        # Check if the problem was a duplicate name
                        if 'InvalidAMIName.Duplicate' in e.message:
                            # Keep trying until an unused name is found.
                            # This probably won't trigger, since it seems
                            # like EC2 doesn't mind duplicate AMI names
                            # when they are being copied, only registered.
                            # Strange, but true.
                            self.dup_count += 1
                            continue
                        else:
                            # TODO: Catch a more specific exception
                            logging.exception(
                                'Image copy to {0} failed'.format(
                                    ami['region']))
                            fedimg.messenger.message('image.upload',
                                                     self.build_name,
                                                     alt_dest, 'failed')
                    break

            # Now cycle through and make all of the copied AMIs public
            # once the copy process has completed.
            amis = self.amis[1:]
            for image in copied_images:
                ami = amis[copied_images.index(image)]
                alt_cls = get_driver(ami['prov'])
                alt_driver = alt_cls(fedimg.AWS_ACCESS_ID,
                                     fedimg.AWS_SECRET_KEY)
                # Need to wait until the copy finishes in order to make
                # the AMI public.
                while True:
                    try:
                        alt_driver.ex_modify_image_attribute(
                            image,
                            {'LaunchPermission.Add.1.Group': 'all'})
                    except Exception as e:
                        if 'InvalidAMIID.Unavailable' in e.message:
                            # Copy isn't done, so wait 20 seconds and try
                            # again.
                            sleep(20)
                            continue
                    break

                logging.info('Made image {0} public'.format(image.name))

                fedimg.messenger.message('image.upload',
                                         self.build_name,
                                         alt_dest, 'completed',
                                         extra={'id': image.id})
