# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class EasyShopView(BrowserView):
    """
    """
    def disableBorder(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if not mtool.checkPermission('Manage portal', self.context):
            self.request.set('disable_border', 1)