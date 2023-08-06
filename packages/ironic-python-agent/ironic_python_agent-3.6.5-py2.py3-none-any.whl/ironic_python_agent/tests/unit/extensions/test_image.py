# Copyright 2015 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import shutil
import tempfile

import mock
from oslo_concurrency import processutils

from ironic_python_agent import errors
from ironic_python_agent.extensions import image
from ironic_python_agent.extensions import iscsi
from ironic_python_agent import hardware
from ironic_python_agent.tests.unit import base
from ironic_python_agent import utils


@mock.patch.object(hardware, 'dispatch_to_managers', autospec=True)
@mock.patch.object(utils, 'execute', autospec=True)
@mock.patch.object(tempfile, 'mkdtemp', lambda *_: '/tmp/fake-dir')
@mock.patch.object(shutil, 'rmtree', lambda *_: None)
class TestImageExtension(base.IronicAgentTest):

    def setUp(self):
        super(TestImageExtension, self).setUp()
        self.agent_extension = image.ImageExtension()
        self.fake_dev = '/dev/fake'
        self.fake_efi_system_part = '/dev/fake1'
        self.fake_root_part = '/dev/fake2'
        self.fake_prep_boot_part = '/dev/fake3'
        self.fake_root_uuid = '11111111-2222-3333-4444-555555555555'
        self.fake_efi_system_part_uuid = '45AB-2312'
        self.fake_prep_boot_part_uuid = '76937797-3253-8843-999999999999'
        self.fake_dir = '/tmp/fake-dir'
        self.agent_extension.agent = mock.Mock()
        self.agent_extension.agent.iscsi_started = True

    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_install_grub2', autospec=True)
    def test__install_bootloader_bios(self, mock_grub2, mock_iscsi_clean,
                                      mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='bios')
        ]
        self.agent_extension.install_bootloader(root_uuid=self.fake_root_uuid)
        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        self.assertEqual(2, mock_dispatch.call_count)
        mock_grub2.assert_called_once_with(
            self.fake_dev, root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None, prep_boot_part_uuid=None)
        mock_iscsi_clean.assert_called_once_with(self.fake_dev)

    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_manage_uefi', autospec=True)
    @mock.patch.object(image, '_install_grub2', autospec=True)
    def test__install_bootloader_uefi(self, mock_grub2, mock_uefi,
                                      mock_iscsi_clean,
                                      mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='uefi')
        ]
        mock_uefi.return_value = False
        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=self.fake_efi_system_part_uuid)
        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        self.assertEqual(2, mock_dispatch.call_count)
        mock_grub2.assert_called_once_with(
            self.fake_dev,
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=self.fake_efi_system_part_uuid,
            prep_boot_part_uuid=None)
        mock_iscsi_clean.assert_called_once_with(self.fake_dev)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=False)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__uefi_bootloader_given_partition(
            self, mkdir_mock, mock_utils_efi_part, mock_partition,
            mock_efi_bl, mock_iscsi_clean, mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='uefi')
        ]
        mock_partition.side_effect = [self.fake_dev, self.fake_efi_system_part]
        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI']
        mock_utils_efi_part.return_value = '1'

        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', '')])

        expected = [mock.call('efibootmgr', '--version'),
                    mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=self.fake_efi_system_part_uuid)

        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        mock_utils_efi_part.assert_called_once_with(self.fake_dev)
        self.assertEqual(8, mock_execute.call_count)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__uefi_bootloader_find_partition(
            self, mkdir_mock, mock_utils_efi_part, mock_partition,
            mock_efi_bl, mock_iscsi_clean, mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='uefi')
        ]
        mock_partition.return_value = self.fake_dev
        mock_utils_efi_part.return_value = '1'
        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI']
        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', '')])

        expected = [mock.call('efibootmgr', '--version'),
                    mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None)

        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        mock_utils_efi_part.assert_called_once_with(self.fake_dev)
        self.assertEqual(8, mock_execute.call_count)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__uefi_bootloader_with_entry_removal(
            self, mkdir_mock, mock_utils_efi_part, mock_partition,
            mock_efi_bl, mock_iscsi_clean, mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='uefi')
        ]
        mock_partition.return_value = self.fake_dev
        mock_utils_efi_part.return_value = '1'
        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI']
        stdeer_msg = """
efibootmgr: ** Warning ** : Boot0004 has same label ironic1\n
efibootmgr: ** Warning ** : Boot0005 has same label ironic1\n
"""
        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', stdeer_msg),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', '')])

        expected = [mock.call('efibootmgr', '--version'),
                    mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('efibootmgr', '-b', '0004', '-B'),
                    mock.call('efibootmgr', '-b', '0005', '-B'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None)

        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        mock_utils_efi_part.assert_called_once_with(self.fake_dev)
        self.assertEqual(10, mock_execute.call_count)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__add_multi_bootloaders(
            self, mkdir_mock, mock_utils_efi_part, mock_partition,
            mock_efi_bl, mock_iscsi_clean, mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='uefi')
        ]
        mock_partition.return_value = self.fake_dev
        mock_utils_efi_part.return_value = '1'
        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI',
                                    '\\WINDOWS\\system32\\winload.efi']

        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', '')])

        expected = [mock.call('efibootmgr', '--version'),
                    mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic2', '-l',
                              '\\WINDOWS\\system32\\winload.efi'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None)

        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        mock_utils_efi_part.assert_called_once_with(self.fake_dev)
        self.assertEqual(9, mock_execute.call_count)

    @mock.patch.object(iscsi, 'clean_up', autospec=True)
    @mock.patch.object(image, '_install_grub2', autospec=True)
    def test__install_bootloader_prep(self, mock_grub2, mock_iscsi_clean,
                                      mock_execute, mock_dispatch):
        mock_dispatch.side_effect = [
            self.fake_dev, hardware.BootInfo(current_boot_mode='bios')
        ]
        self.agent_extension.install_bootloader(
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None,
            prep_boot_part_uuid=self.fake_prep_boot_part_uuid)
        mock_dispatch.assert_any_call('get_os_install_device')
        mock_dispatch.assert_any_call('get_boot_info')
        self.assertEqual(2, mock_dispatch.call_count)
        mock_grub2.assert_called_once_with(
            self.fake_dev,
            root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=None,
            prep_boot_part_uuid=self.fake_prep_boot_part_uuid)
        mock_iscsi_clean.assert_called_once_with(self.fake_dev)

    @mock.patch.object(os, 'environ', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2(self, mock_get_part_uuid, environ_mock,
                            mock_execute, mock_dispatch):
        mock_get_part_uuid.return_value = self.fake_root_part
        environ_mock.get.return_value = '/sbin'
        image._install_grub2(self.fake_dev, self.fake_root_uuid)

        expected = [mock.call('mount', '/dev/fake2', self.fake_dir),
                    mock.call('mount', '-o', 'bind', '/dev',
                              self.fake_dir + '/dev'),
                    mock.call('mount', '-o', 'bind', '/proc',
                              self.fake_dir + '/proc'),
                    mock.call('mount', '-o', 'bind', '/run',
                              self.fake_dir + '/run'),
                    mock.call('mount', '-t', 'sysfs', 'none',
                              self.fake_dir + '/sys'),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s"' %
                               (self.fake_dir, self.fake_dev)), shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                               '"grub-mkconfig -o '
                               '/boot/grub/grub.cfg"' % self.fake_dir),
                              shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call('umount', self.fake_dir + '/dev',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/proc',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/run',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/sys',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir, attempts=3,
                              delay_on_retry=True)]
        mock_execute.assert_has_calls(expected)
        mock_get_part_uuid.assert_called_once_with(self.fake_dev,
                                                   uuid=self.fake_root_uuid)
        self.assertFalse(mock_dispatch.called)

    @mock.patch.object(os, 'environ', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2_prep(self, mock_get_part_uuid, environ_mock,
                                 mock_execute, mock_dispatch):
        mock_get_part_uuid.side_effect = [self.fake_root_part,
                                          self.fake_prep_boot_part]
        environ_mock.get.return_value = '/sbin'
        image._install_grub2(self.fake_dev, self.fake_root_uuid,
                             prep_boot_part_uuid=self.fake_prep_boot_part_uuid)

        expected = [mock.call('mount', '/dev/fake2', self.fake_dir),
                    mock.call('mount', '-o', 'bind', '/dev',
                              self.fake_dir + '/dev'),
                    mock.call('mount', '-o', 'bind', '/proc',
                              self.fake_dir + '/proc'),
                    mock.call('mount', '-o', 'bind', '/run',
                              self.fake_dir + '/run'),
                    mock.call('mount', '-t', 'sysfs', 'none',
                              self.fake_dir + '/sys'),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s"' %
                               (self.fake_dir, self.fake_prep_boot_part)),
                              shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                               '"grub-mkconfig -o '
                               '/boot/grub/grub.cfg"' % self.fake_dir),
                              shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call('umount', self.fake_dir + '/dev',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/proc',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/run',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/sys',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir, attempts=3,
                              delay_on_retry=True)]
        mock_execute.assert_has_calls(expected)
        mock_get_part_uuid.assert_any_call(self.fake_dev,
                                           uuid=self.fake_root_uuid)
        mock_get_part_uuid.assert_any_call(self.fake_dev,
                                           uuid=self.fake_prep_boot_part_uuid)
        self.assertFalse(mock_dispatch.called)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(os, 'environ', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2_uefi(self, mock_get_part_uuid, mkdir_mock,
                                 environ_mock, mock_execute,
                                 mock_dispatch):
        mock_get_part_uuid.side_effect = [self.fake_root_part,
                                          self.fake_efi_system_part]
        environ_mock.get.return_value = '/sbin'

        image._install_grub2(
            self.fake_dev, root_uuid=self.fake_root_uuid,
            efi_system_part_uuid=self.fake_efi_system_part_uuid)

        expected = [mock.call('mount', '/dev/fake2', self.fake_dir),
                    mock.call('mount', '-o', 'bind', '/dev',
                              self.fake_dir + '/dev'),
                    mock.call('mount', '-o', 'bind', '/proc',
                              self.fake_dir + '/proc'),
                    mock.call('mount', '-o', 'bind', '/run',
                              self.fake_dir + '/run'),
                    mock.call('mount', '-t', 'sysfs', 'none',
                              self.fake_dir + '/sys'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s"' %
                               (self.fake_dir, self.fake_dev)), shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s --removable"' %
                               (self.fake_dir, self.fake_dev)), shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                               '"grub-mkconfig -o '
                               '/boot/grub/grub.cfg"' % self.fake_dir),
                              shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/dev',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/proc',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/run',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/sys',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir, attempts=3,
                              delay_on_retry=True)]
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        mock_get_part_uuid.assert_any_call(self.fake_dev,
                                           uuid=self.fake_root_uuid)
        mock_get_part_uuid.assert_any_call(self.fake_dev,
                                           uuid=self.fake_efi_system_part_uuid)
        self.assertFalse(mock_dispatch.called)

    @mock.patch.object(os, 'environ', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2_uefi_umount_fails(
            self, mock_get_part_uuid, mkdir_mock, environ_mock, mock_execute,
            mock_dispatch):
        mock_get_part_uuid.side_effect = [self.fake_root_part,
                                          self.fake_efi_system_part]

        def umount_raise_func(*args, **kwargs):
            if args[0] == 'umount':
                raise processutils.ProcessExecutionError('error')

        mock_execute.side_effect = umount_raise_func
        environ_mock.get.return_value = '/sbin'
        self.assertRaises(errors.CommandExecutionError,
                          image._install_grub2,
                          self.fake_dev, root_uuid=self.fake_root_uuid,
                          efi_system_part_uuid=self.fake_efi_system_part_uuid)

        expected = [mock.call('mount', '/dev/fake2', self.fake_dir),
                    mock.call('mount', '-o', 'bind', '/dev',
                              self.fake_dir + '/dev'),
                    mock.call('mount', '-o', 'bind', '/proc',
                              self.fake_dir + '/proc'),
                    mock.call('mount', '-o', 'bind', '/run',
                              self.fake_dir + '/run'),
                    mock.call('mount', '-t', 'sysfs', 'none',
                              self.fake_dir + '/sys'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s"' %
                               (self.fake_dir, self.fake_dev)), shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                              '"grub-install %s --removable"' %
                               (self.fake_dir, self.fake_dev)), shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call(('chroot %s /bin/sh -c '
                               '"grub-mkconfig -o '
                               '/boot/grub/grub.cfg"' % self.fake_dir),
                              shell=True,
                              env_variables={'PATH': '/sbin:/bin:/usr/sbin'}),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True)]
        mock_execute.assert_has_calls(expected)

    @mock.patch.object(os, 'environ', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2_uefi_mount_fails(
            self, mock_get_part_uuid, mkdir_mock, environ_mock, mock_execute,
            mock_dispatch):
        mock_get_part_uuid.side_effect = [self.fake_root_part,
                                          self.fake_efi_system_part]

        def mount_raise_func(*args, **kwargs):
            if args[0] == 'mount':
                raise processutils.ProcessExecutionError('error')

        mock_execute.side_effect = mount_raise_func
        self.assertRaises(errors.CommandExecutionError,
                          image._install_grub2,
                          self.fake_dev, root_uuid=self.fake_root_uuid,
                          efi_system_part_uuid=self.fake_efi_system_part_uuid)

        expected = [mock.call('mount', '/dev/fake2', self.fake_dir),
                    mock.call('umount', self.fake_dir + '/dev',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/proc',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/run',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir + '/sys',
                              attempts=3, delay_on_retry=True),
                    mock.call('umount', self.fake_dir, attempts=3,
                              delay_on_retry=True)]
        mock_execute.assert_has_calls(expected)

    @mock.patch.object(image, '_get_partition', autospec=True)
    def test__install_grub2_command_fail(self, mock_get_part_uuid,
                                         mock_execute,
                                         mock_dispatch):
        mock_get_part_uuid.return_value = self.fake_root_part
        mock_execute.side_effect = processutils.ProcessExecutionError('boom')

        self.assertRaises(errors.CommandExecutionError, image._install_grub2,
                          self.fake_dev, self.fake_root_uuid)

        mock_get_part_uuid.assert_called_once_with(self.fake_dev,
                                                   uuid=self.fake_root_uuid)
        self.assertFalse(mock_dispatch.called)

    def test__get_partition(self, mock_execute, mock_dispatch):
        lsblk_output = ('''KNAME="test" UUID="" TYPE="disk"
        KNAME="test1" UUID="256a39e3-ca3c-4fb8-9cc2-b32eec441f47" TYPE="part"
        KNAME="test2" UUID="%s" TYPE="part"''' % self.fake_root_uuid)
        mock_execute.side_effect = (None, None, [lsblk_output])

        root_part = image._get_partition(self.fake_dev, self.fake_root_uuid)
        self.assertEqual('/dev/test2', root_part)
        expected = [mock.call('partx', '-u', self.fake_dev, attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('lsblk', '-PbioKNAME,UUID,PARTUUID,TYPE',
                              self.fake_dev)]
        mock_execute.assert_has_calls(expected)
        self.assertFalse(mock_dispatch.called)

    def test__get_partition_no_device_found(self, mock_execute,
                                            mock_dispatch):
        lsblk_output = ('''KNAME="test" UUID="" TYPE="disk"
        KNAME="test1" UUID="256a39e3-ca3c-4fb8-9cc2-b32eec441f47" TYPE="part"
        KNAME="test2" UUID="" TYPE="part"''')
        mock_execute.side_effect = (None, None, [lsblk_output])

        self.assertRaises(errors.DeviceNotFound,
                          image._get_partition, self.fake_dev,
                          self.fake_root_uuid)
        expected = [mock.call('partx', '-u', self.fake_dev, attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('lsblk', '-PbioKNAME,UUID,PARTUUID,TYPE',
                              self.fake_dev)]
        mock_execute.assert_has_calls(expected)
        self.assertFalse(mock_dispatch.called)

    def test__get_partition_command_fail(self, mock_execute,
                                         mock_dispatch):
        mock_execute.side_effect = (None, None,
                                    processutils.ProcessExecutionError('boom'))
        self.assertRaises(errors.CommandExecutionError,
                          image._get_partition, self.fake_dev,
                          self.fake_root_uuid)

        expected = [mock.call('partx', '-u', self.fake_dev, attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('lsblk', '-PbioKNAME,UUID,PARTUUID,TYPE',
                              self.fake_dev)]
        mock_execute.assert_has_calls(expected)
        self.assertFalse(mock_dispatch.called)

    def test__get_partition_partuuid(self, mock_execute, mock_dispatch):
        lsblk_output = ('''KNAME="test" UUID="" TYPE="disk"
        KNAME="test1" UUID="256a39e3-ca3c-4fb8-9cc2-b32eec441f47" TYPE="part"
        KNAME="test2" PARTUUID="%s" TYPE="part"''' % self.fake_root_uuid)
        mock_execute.side_effect = (None, None, [lsblk_output])

        root_part = image._get_partition(self.fake_dev, self.fake_root_uuid)
        self.assertEqual('/dev/test2', root_part)
        expected = [mock.call('partx', '-u', self.fake_dev, attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('lsblk', '-PbioKNAME,UUID,PARTUUID,TYPE',
                              self.fake_dev)]
        mock_execute.assert_has_calls(expected)
        self.assertFalse(mock_dispatch.called)

    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    def test__manage_uefi_no_partition(self, mock_utils_efi_part,
                                       mock_get_part_uuid,
                                       mock_execute, mock_dispatch):
        mock_utils_efi_part.return_value = None
        mock_get_part_uuid.return_value = self.fake_root_part
        result = image._manage_uefi(self.fake_dev, self.fake_root_uuid)
        self.assertFalse(result)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__manage_uefi(self, mkdir_mock, mock_utils_efi_part,
                          mock_get_part_uuid, mock_efi_bl, mock_execute,
                          mock_dispatch):
        mock_utils_efi_part.return_value = '1'
        mock_get_part_uuid.return_value = self.fake_dev

        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI']

        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', '')])

        expected = [mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        result = image._manage_uefi(self.fake_dev, self.fake_root_uuid)
        self.assertTrue(result)
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        self.assertEqual(7, mock_execute.call_count)

    @mock.patch.object(os.path, 'exists', lambda *_: False)
    @mock.patch.object(image, '_get_efi_bootloaders', autospec=True)
    @mock.patch.object(image, '_get_partition', autospec=True)
    @mock.patch.object(utils, 'get_efi_part_on_device', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test__manage_uefi_wholedisk(
            self, mkdir_mock, mock_utils_efi_part,
            mock_get_part_uuid, mock_efi_bl, mock_execute,
            mock_dispatch):
        mock_utils_efi_part.return_value = '1'
        mock_get_part_uuid.side_effect = Exception

        mock_efi_bl.return_value = ['\\EFI\\BOOT\\BOOTX64.EFI']

        mock_execute.side_effect = iter([('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', ''), ('', ''),
                                         ('', '')])

        expected = [mock.call('partx', '-u', '/dev/fake', attempts=3,
                              delay_on_retry=True),
                    mock.call('udevadm', 'settle'),
                    mock.call('mount', self.fake_efi_system_part,
                              self.fake_dir + '/boot/efi'),
                    mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', '1', '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI'),
                    mock.call('umount', self.fake_dir + '/boot/efi',
                              attempts=3, delay_on_retry=True),
                    mock.call('sync')]

        result = image._manage_uefi(self.fake_dev, None)
        self.assertTrue(result)
        mkdir_mock.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_efi_bl.assert_called_once_with(self.fake_dir + '/boot/efi')
        mock_execute.assert_has_calls(expected)
        self.assertEqual(7, mock_execute.call_count)

    @mock.patch.object(os, 'walk', autospec=True)
    @mock.patch.object(os, 'access', autospec=False)
    def test__no_efi_bootloaders(self, mock_access, mock_walk, mock_execute,
                                 mock_dispatch):
        # No valid efi file.
        mock_walk.return_value = [
            ('/boot/efi', ['EFI'], []),
            ('/boot/efi/EFI', ['centos', 'BOOT'], []),
            ('/boot/efi/EFI/centos', ['fw', 'fonts'],
             ['shimx64-centos.efi', 'BOOT.CSV', 'BOOTX64.CSV',
              'MokManager.efi', 'mmx64.efi', 'shim.efi', 'fwupia32.efi',
              'fwupx64.efi', 'shimx64.efi', 'grubenv', 'grubx64.efi',
              'grub.cfg']),
            ('/boot/efi/EFI/centos/fw', [], []),
            ('/boot/efi/EFI/centos/fonts', [], ['unicode.pf2']),
            ('/boot/efi/EFI/BOOT', [], [])
        ]

        result = image._get_efi_bootloaders("/boot/efi")
        self.assertEqual(result, [])
        mock_access.assert_not_called()

    @mock.patch.object(os, 'walk', autospec=True)
    @mock.patch.object(os, 'access', autospec=True)
    def test__get_efi_bootloaders(self, mock_access, mock_walk, mock_execute,
                                  mock_dispatch):
        mock_walk.return_value = [
            ('/boot/efi', ['EFI'], []),
            ('/boot/efi/EFI', ['centos', 'BOOT'], []),
            ('/boot/efi/EFI/centos', ['fw', 'fonts'],
             ['shimx64-centos.efi', 'BOOT.CSV', 'BOOTX64.CSV',
              'MokManager.efi', 'mmx64.efi', 'shim.efi', 'fwupia32.efi',
              'fwupx64.efi', 'shimx64.efi', 'grubenv', 'grubx64.efi',
              'grub.cfg']),
            ('/boot/efi/EFI/centos/fw', [], []),
            ('/boot/efi/EFI/centos/fonts', [], ['unicode.pf2']),
            ('/boot/efi/EFI/BOOT', [],
             ['BOOTX64.EFI', 'fallback.efi', 'fbx64.efi'])
        ]
        mock_access.return_value = True
        result = image._get_efi_bootloaders("/boot/efi")
        self.assertEqual(result[0], '\\EFI\\BOOT\\BOOTX64.EFI')

    @mock.patch.object(os, 'walk', autospec=True)
    @mock.patch.object(os, 'access', autospec=True)
    def test__get_windows_efi_bootloaders(self, mock_access, mock_walk,
                                          mock_execute, mock_dispatch):
        mock_walk.return_value = [
            ('/boot/efi', ['WINDOWS'], []),
            ('/boot/efi/WINDOWS', ['system32'], []),
            ('/boot/efi/WINDOWS/system32', [],
             ['winload.efi'])
        ]
        mock_access.return_value = True
        result = image._get_efi_bootloaders("/boot/efi")
        self.assertEqual(result[0], '\\WINDOWS\\system32\\winload.efi')

    def test__run_efibootmgr_no_bootloaders(self, mock_execute, mock_dispatch):
        result = image._run_efibootmgr([], self.fake_dev,
                                       self.fake_efi_system_part)
        expected = []
        self.assertIsNone(result)
        mock_execute.assert_has_calls(expected)

    def test__run_efibootmgr(self, mock_execute, mock_dispatch):
        result = image._run_efibootmgr(['\\EFI\\BOOT\\BOOTX64.EFI'],
                                       self.fake_dev,
                                       self.fake_efi_system_part)
        expected = [mock.call('efibootmgr'),
                    mock.call('efibootmgr', '-c', '-d', self.fake_dev,
                              '-p', self.fake_efi_system_part, '-w',
                              '-L', 'ironic1', '-l',
                              '\\EFI\\BOOT\\BOOTX64.EFI')]
        self.assertIsNone(result)
        mock_execute.assert_has_calls(expected)
