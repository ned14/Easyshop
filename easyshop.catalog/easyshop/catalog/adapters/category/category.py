# Zope imports
from zope.interface import implements
from zope.component import adapts

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

    def hasCategories(self):
        """
        """
        if len(self.getCategories()) > 0:
            return True
        return False

    def hasParentCategory(self):
        """
        """
        if self.context.aq_inner.aq_parent.portal_type == "Category":
            return True
        return False
        
    def getCategories(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Category",
            path = {"query"       : "/".join(self.context.getPhysicalPath()),
                    "depth"       : 1},
        )

        return brains

    def getTotalCategories(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        
        brains = catalog(portal_type="Category",
                         path = "/".join(self.context.getPhysicalPath()),
                         sort_on = "getObjPositionInParent")

        # Todo: Optimize
        return [brain.getObject() for brain in brains
                                  if brain.getId != self.context.getId()]