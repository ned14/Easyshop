# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShop

class ShopCategoryManagement:
    """An adapter which provides ICategoryManagement for shop content objects.
    """
    implements(ICategoryManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.categories = context.categories

    def hasCategories(self):
        """
        """
        if len(self.getCategories()) > 0:
            return True
        return False

    def hasParentCategory(self):
        """
        """
        return False
        if self.context.aq_inner.aq_parent.portal_type == "Category":
            return True
        return False
        
    def getCategories(self):
        """
        """        
        # Todo: Check whether brains can be returned
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.categories.getPhysicalPath()),
            portal_type="Category",
            sort_on = "getObjPositionInParent")

        return brains
    
    def getTopLevelCategories(self):
        """
        """ 
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(portal_type="Category",
                         path = {"query" : "/".join(self.categories.getPhysicalPath()),
                                 "depth" : 1},
                         sort_on = "getObjPositionInParent")
        return brains