# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct

class ProductCategoryManager:
    """Provides ICategoryManagement for product content objects.
    """
    implements(ICategoryManagement)
    adapts(IProduct)

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
        return False

    def getCategories(self):
        """Returns all categories of the product
        """
        # Need the try/except here, because the of the temporary created
        # shipping product, which has no context and hence no access to 
        # tools and catalogs (and it doesn't need it, but I have to catch 
        # the error.)
        try:
            mtool = getToolByName(self.context, "portal_membership")            
            categories = self.context.getBRefs("easyshopcategory_easyshopproduct")
        except AttributeError:
            return []

        result = []
        for category in categories:
            if mtool.checkPermission("View", category):
                result.append(category)
            
        return result