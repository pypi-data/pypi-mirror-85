# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.targetblank.testing import COLLECTIVE_BEHAVIOR_TARGETBLANK_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.behavior.targetblank is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_TARGETBLANK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.behavior.targetblank is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.behavior.targetblank'))

    def test_browserlayer(self):
        """Test that ICollectiveBehaviorTargetblankLayer is registered."""
        from collective.behavior.targetblank.interfaces import (
            ICollectiveBehaviorTargetblankLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveBehaviorTargetblankLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_TARGETBLANK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.behavior.targetblank'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.behavior.targetblank is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.behavior.targetblank'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBehaviorTargetblankLayer is removed."""
        from collective.behavior.targetblank.interfaces import \
            ICollectiveBehaviorTargetblankLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveBehaviorTargetblankLayer,
            utils.registered_layers())
