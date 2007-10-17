# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class IPortletEasyShopAdministrationView(Interface):    
    """
    """
    def getShopURL():
        """Returns the URL of the shop.
        """

    def showPortlet():
        """Returns True if the portlet is allowed to be shown.
        """
        
class PortletEasyShopAdministrationView(BrowserView):
    """
    """
    implements(IPortletEasyShopAdministrationView)
    
    def getShopURL(self):
        """
        """
        return self.context.getShop().absolute_url()
        
    def showPortlet(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        else:
            return False