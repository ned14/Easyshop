# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShop

class CategoryCategoryManagement(object):
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
        self.categories = []
        
        for category in self.getTopLevelCategories():
            
            self.categories.append(category)
            self._getCategories(category)
        
        return self.categories

    def _getCategories(self, parent_category):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")

        for category in parent_category.getBRefs("parent_category"):

            if mtool.checkPermission("View", category) == True:
                self.categories.append(category)
                self._getCategories(category)
        
    def getTopLevelCategories(self):
        """Returns objects.
        """
        mtool = getToolByName(self.context, "portal_membership")
        return [c for c in self.context.getBRefs("parent_category") 
                           if mtool.checkPermission("View", c) == True]

        
class ProductCategoryManagement(object):
    """Adapter which provides ICategoryManagement for product content objects.
    """
    implements(ICategoryManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """
        """
        return self.context.getCategories()
        
    def getTopLevelCategories(self):
        """Returns objects.
        """
        # Need the try/except here, because the temporary created shipping 
        # product, which has no context and hence no access to tools and 
        # catalogs (and it doesn't need it, but I have to catch the error.)
        try:
            mtool = getToolByName(self.context, "portal_membership")            
            categories = self.context.getBRefs("categories_products")
        except AttributeError:
            return []

        result = []
        for category in categories:

            if mtool.checkPermission("View", category):
                result.append(category)
        
        return result
        
class ShopCategoryManagement(object):
    """An adapter which provides ICategoryManagement for shop content objects.
    """
    implements(ICategoryManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getCategories(self):
        """Returns brains.
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.getPhysicalPath()),
            object_provides="easyshop.core.interfaces.catalog.ICategory",
            sort_on = "getObjPositionInParent")

        return brains
    
    def getTopLevelCategories(self):
        """Returns objects.
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for category in self.context.objectValues("Category"):

            if mtool.checkPermission("View", category) != True:
                continue

            if len(category.getRefs("parent_category")) == 0:
                result.append(category)
            
        return result