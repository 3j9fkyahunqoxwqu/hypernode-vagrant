from hypernode_vagrant_runner.settings import HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION
from hypernode_vagrant_runner.vagrant import hypernode_vagrant
from tests.testcase import TestCase


class TestHypernodeVagrant(TestCase):
    def setUp(self):
        self.create_hypernode_vagrant = self.set_up_patch(
            'hypernode_vagrant_runner.vagrant.create_hypernode_vagrant'
        )
        self.get_networking_information_from_vagrant = self.set_up_patch(
            'hypernode_vagrant_runner.vagrant.get_networking_information_from_vagrant'
        )
        self.destroy_hypernode_vagrant = self.set_up_patch(
            'hypernode_vagrant_runner.vagrant.destroy_hypernode_vagrant'
        )
        self.remove_hypernode_vagrant = self.set_up_patch(
            'hypernode_vagrant_runner.vagrant.remove_hypernode_vagrant'
        )

    def test_hypernode_vagrant_creates_hypernode_vagrant_before_context(self):
        with hypernode_vagrant():
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=False,
                skip_try_sudo=False,
                xenial=False,
                no_provision=False
            )

    def test_hypernode_vagrant_creates_hypernode_vagrant_using_specified_checkout(self):
        with hypernode_vagrant(
                directory='/your/already/checked/out/hypernode-vagrant'
        ):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory='/your/already/checked/out/hypernode-vagrant',
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=False,
                skip_try_sudo=False,
                xenial=False,
                no_provision=False
            )

    def test_hypernode_vagrant_creates_hypernode_vagrant_of_specified_php_version(self):
        with hypernode_vagrant(php_version='7.0'):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version='7.0',
                xdebug_enabled=False,
                skip_try_sudo=False,
                xenial=False,
                no_provision=False
            )

    def test_hypernode_vagrant_creates_hypernode_vagrant_with_xdebug_enabled_if_specified(self):
        with hypernode_vagrant(xdebug_enabled=True):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=True,
                skip_try_sudo=False,
                xenial=False,
                no_provision=False
            )

    def test_hypernode_vagrant_creates_hypernode_vagrant_with_xenial_image_if_specified(self):
        with hypernode_vagrant(xenial=True):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=False,
                skip_try_sudo=False,
                xenial=True,
                no_provision=False
            )

    def test_hypernode_vagrant_skips_try_sudo_if_specified(self):
        with hypernode_vagrant(skip_try_sudo=True):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=False,
                skip_try_sudo=True,
                xenial=False,
                no_provision=False
            )

    def test_hypernode_vagrant_skips_provisioning_if_specified(self):
        with hypernode_vagrant(no_provision=True):
            self.create_hypernode_vagrant.assert_called_once_with(
                directory=None,
                php_version=HYPERNODE_VAGRANT_DEFAULT_PHP_VERSION,
                xdebug_enabled=False,
                skip_try_sudo=False,
                xenial=False,
                no_provision=True
            )

    def test_hypernode_vagrant_destroys_hypernode_vagrant_after_context(self):
        with hypernode_vagrant():
            self.assertFalse(self.destroy_hypernode_vagrant.called)
        self.destroy_hypernode_vagrant.assert_called_once_with(
            self.create_hypernode_vagrant.return_value
        )

    def test_hypernode_vagrant_removes_hypernode_vagrant_after_context(self):
        with hypernode_vagrant():
            self.assertFalse(self.remove_hypernode_vagrant.called)
        self.remove_hypernode_vagrant.assert_called_once_with(
            self.create_hypernode_vagrant.return_value
        )

    def test_hypernode_vagrant_does_not_destroy_hypernode_vagrant_if_pre_existing_directory_used(self):
        with hypernode_vagrant(directory='/tmp/some/directory'):
            pass
        self.assertFalse(self.destroy_hypernode_vagrant.called)

    def test_hypernode_vagrant_does_not_remove_hypernode_vagrant_if_pre_existing_directory_used(self):
        with hypernode_vagrant(directory='/tmp/some/directory'):
            pass
        self.assertFalse(self.remove_hypernode_vagrant.called)

    def test_hypernode_vagrant_yields_vagrant_networking_information(self):
        with hypernode_vagrant() as information:
            self.assertEqual(
                information, self.get_networking_information_from_vagrant.return_value
            )

    def test_hypernode_vagrant_gets_networking_information_from_created_vagrant(self):
        with hypernode_vagrant():
            self.get_networking_information_from_vagrant.assert_called_once_with(
                self.create_hypernode_vagrant.return_value
            )
