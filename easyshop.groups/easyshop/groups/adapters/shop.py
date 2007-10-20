# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IGroupManagement
from Products.EasyShop.interfaces import IShopContent

class ShopGroupManagement:
    """An adapter, which provides group management for shop content objects.
    """
    implements(IGroupManagement)
    adapts(IShopContent)
        
    def __init__(self, context):
        """
        """
        self.context = context

    def getGroups(self):
        """Returns all groups
        """
        # XXX: Optimize
        return self.context.groups.objectValues("ProductGroup")