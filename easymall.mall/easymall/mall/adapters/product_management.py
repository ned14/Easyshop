# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement
from easyshop.catalog.adapters.product_management \
    import CategoryProductManagement as EasyShopCategoryProductManagement
    
# easymall imports
from easymall.mall.interfaces import IMall

class CategoryProductManagement(EasyShopCategoryProductManagement):
    """An adapter which provides IProductManagement for category content
    objects.
    """
    def getProducts(self, category_id=None):
        """
        """
        shop_or_mall = IShopManagement(self.context).getShop()

        # NOTE: The more specific one has to be the first, because a mall is 
        # also a shop
        if IMall.providedBy(shop_or_mall):
            reference = "mall_categories_products"
        elif IShop.providedBy(shop_or_mall):
            reference = "categories_products"            
        else:
            return []
        
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs(reference):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result