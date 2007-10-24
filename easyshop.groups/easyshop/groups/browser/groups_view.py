# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IShopManagement

class IGroupsView(Interface):    
    """
    """
    def getGroups():
        """Returns groups of the shop.
        """
           
class GroupsView(BrowserView):
    """
    """
    implements(IGroupsView)
    
    def getGroups(self):
        """Returns groups of the shop.
        """
        shop = IShopManagement(self.context).getShop()
        
        gm = IGroupManagement(shop)
        return gm.getGroups()
    