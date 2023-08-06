# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.behavior.targetblank import _
from plone import api
from plone.app.contenttypes.interfaces import ILink
from plone.autoform.interfaces import IFormFieldProvider
from plone.indexer import indexer
from plone.supermodel import model
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.browser.navigation import get_id
from Products.CMFPlone.browser.navigation import get_view_url
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class TargetBlankCatalogNavigationTabs(CatalogNavigationTabs):
    def topLevelTabs(self, actions=None, category='portal_tabs'):
        """This method is copy/paste from CatalogNavigationTabs,
        Only link_target is added on last lines
        """
        context = aq_inner(self.context)

        mtool = api.portal.get_tool('portal_membership')
        member = mtool.getAuthenticatedMember().id  # noqa

        portal_properties = api.portal.get_tool('portal_properties')
        self.navtree_properties = getattr(portal_properties,
                                          'navtree_properties')
        self.site_properties = getattr(portal_properties,
                                       'site_properties')
        self.portal_catalog = api.portal.get_tool('portal_catalog')

        if actions is None:
            context_state = api.content.get_view(
                'plone_context_state', context, self.request)
            actions = context_state.actions(category)

        # Build result dict
        result = []
        # first the actions
        if actions is not None:
            for actionInfo in actions:
                data = actionInfo.copy()
                data['name'] = data['title']
                result.append(data)

        # check whether we only want actions
        if self.site_properties.getProperty('disable_folder_sections', False):
            return result

        query = self._getNavQuery()

        rawresult = self.portal_catalog.searchResults(query)  # noqa

        def get_link_url(item):
            linkremote = item.getRemoteUrl and not member == item.Creator
            if linkremote:
                return (get_id(item), item.getRemoteUrl)
            else:
                return False

        # now add the content to results
        idsNotToList = self.navtree_properties.getProperty('idsNotToList', ())
        for item in rawresult:
            if not (item.getId in idsNotToList or item.exclude_from_nav):
                id, item_url = get_link_url(item) or get_view_url(item)
                data = {'name': utils.pretty_title_or_id(context, item),
                        'id': item.getId,
                        'url': item_url,
                        'description': item.Description,
                        'link_target': getattr(item, 'link_target', False)}
                result.append(data)

        return result


class ITargetBlankMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ITargetBlank(model.Schema):
    """
    """

    target_blank = schema.Bool(
        title=_(u'Target blank'),
        description=_(u'Open link in target blank?'),
        default=False,
    )


@implementer(ITargetBlank)
@adapter(ITargetBlankMarker)
class TargetBlank(object):
    def __init__(self, context):
        self.context = context

    @property
    def target_blank(self):
        if getattr(self.context, 'target_blank', False):
            return self.context.target_blank
        return False

    @target_blank.setter
    def target_blank(self, value):
        self.context.target_blank = value


@indexer(ILink)
def link_target_indexer(obj):
    target_blank = getattr(obj, 'target_blank', None)
    if target_blank:
        return '_blank'
    return ''
