# Zope imports
from zope.interface import implements
from zope.component import adapts

# AdvancedQuery
from Products.AdvancedQuery import Eq
 
# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import ICategory

class CategoryCategoryManagement:
    """Adapter which provides ICategoryManagement for category content 
    objects.
    """
    implements(ICategoryManagement)
    adapts(ICategory)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """
        query = Eq("portal_type", "Category") & \
                Eq("path", "/".join(self.context.getPhysicalPath())) & \
                ~ Eq("id", self.context.getId())
        
        
        catalog = getToolByName(self.context, "portal_catalog")
        
        brains = catalog.evalAdvancedQuery(
                        query, ("getObjPositionInParent", ))

        return brains
                                  
    def getTopLevelCategories(self):
        """Returns brains
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Category",
            path = {"query"       : "/".join(self.context.getPhysicalPath()),
                    "depth"       : 1},
        )

        return brains