# zope imports
from zope.interface import implements
from zope.interface import Interface

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShopManagement

class IAdminPortletView(Interface):
    """
    """
    def available():
        """
        """

    def getShopURL():
        """
        """

class AdminPortletView(BrowserView):
    """
    """
    implements(IAdminPortletView)
    
    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        else:
            return False

    def getShopURL(self):
        """
        """
        return IShopManagement(self.context).getShop().absolute_url()