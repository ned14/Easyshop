# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.catalog.adapters.category_management \
    import ProductCategoryManagement

# easymall imports
from easymall.mall.interfaces import IMallProduct
    
class MallProductCategoryManagement(ProductCategoryManagement):
    """Adapter which provides ICategoryManagement for mall product content objects.
    """
    implements(ICategoryManagement)
    adapts(IMallProduct)

    def getTopLevelMallCategories(self):
        """
        """
        # Need the try/except here, because the temporary created shipping 
        # product, which has no context and hence no access to tools and 
        # catalogs (and it doesn't need it, but I have to catch the error.)
        try:
            mtool = getToolByName(self.context, "portal_membership")
            categories = self.context.getBRefs("mall_categories_products")
        except AttributeError:
            return []

        result = []
        for category in categories:
            if mtool.checkPermission("View", category):
                result.append(category)
        
        return result