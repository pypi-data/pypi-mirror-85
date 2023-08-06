# -*- coding: utf-8 -*-
from collective.behavior.targetblank.behaviors.target_blank import ITargetBlank
from collective.behavior.targetblank.behaviors.target_blank import ITargetBlankMarker  # noqa
from collective.behavior.targetblank.behaviors.target_blank import TargetBlankCatalogNavigationTabs  # noqa
from collective.behavior.targetblank.testing import COLLECTIVE_BEHAVIOR_TARGETBLANK_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify

import unittest


class TargetBlankIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_TARGETBLANK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # add target blank behavior to Link
        fti = queryUtility(IDexterityFTI, name='Link')
        behaviors = list(fti.behaviors)
        behaviors.append(ITargetBlank.__identifier__)
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent('Link'))
        # with api.env.adopt_roles(['Manager']):
        self.link = api.content.create(
            self.portal, 'Link', 'my link', remoteUrl='https://www.imio.be')

    def test_behavior_target_blank(self):
        behavior = getUtility(
            IBehavior,
            'collective.behavior.targetblank.behaviors.target_blank',
        )
        self.assertEqual(
            behavior.marker,
            ITargetBlankMarker,
        )

    def test_behavior_target_blank_in_menu(self):
        self.link.target_blank = True
        self.link.reindexObject()
        view = TargetBlankCatalogNavigationTabs(self.portal, self.request)
        topleveltabs = view.topLevelTabs()
        self.assertEqual(topleveltabs[1].get('link_target'), '_blank')

    def test_link_target_index(self):
        catalog = api.portal.get_tool('portal_catalog')

        self.link.target_blank = False
        self.link.reindexObject()
        self.assertEqual(catalog(UID=self.link.UID())[0].link_target, '')

        self.link.target_blank = True
        self.link.reindexObject()
        self.assertEqual(catalog(UID=self.link.UID())[0].link_target, '_blank')
