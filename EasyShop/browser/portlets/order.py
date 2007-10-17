# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class IPortletOrdersView(Interface):    
    """
    """
    def getShopUrl():
        """Returns the url of the parent shop.
        """ 
       
class PortletOrdersView(BrowserView):
    """
    """
    implements(IPortletOrdersView)
    
    def getShopUrl(self):
        """
        """
        