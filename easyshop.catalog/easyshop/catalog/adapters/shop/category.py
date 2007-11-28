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

    def getCategories(self):
        """Returns brains
        """        
        # Todo: Check whether brains can be returned
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.categories.getPhysicalPath()),
            portal_type="Category",
            sort_on = "getObjPositionInParent")

        return brains
    
    def getTopLevelCategories(self):
        """Return brains.
        """ 
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(portal_type="Category",
                         path = {"query" : "/".join(self.categories.getPhysicalPath()),
                                 "depth" : 1},
                         sort_on = "getObjPositionInParent")

        return brains
