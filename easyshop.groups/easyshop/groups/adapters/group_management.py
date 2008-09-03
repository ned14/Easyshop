# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IShop

class ShopGroupManagement:
    """An adapter, which provides group management for shop content objects.
    """
    implements(IGroupManagement)
    adapts(IShop)
        
    def __init__(self, context):
        """
        """
        self.context = context

    def addGroup(self, name):
        """
        """
        putils = getToolByName(self.context, "plone_utils")
        normalized_id = putils.normalizeString(name)
        if self.getGroup(normalized_id) is None:
            self.context.groups.manage_addProduct["easyshop.core"].addProductGroup(id=normalized_id, title=name)
            return self.getGroup(normalized_id)

        else:
            return False
        
    def deleteGroup(id):
        """
        """
        raise Exception
                
    def getGroup(self, group_id):
        """
        """
        return self.context.groups.get(group_id)
        
    def getGroups(self):
        """Returns all groups
        """
        # XXX: Optimize
        return self.context.groups.objectValues("ProductGroup")
        
    def hasGroups():
        """
        """
        raise Exception