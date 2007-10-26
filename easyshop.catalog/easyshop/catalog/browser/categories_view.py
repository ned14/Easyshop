# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class CategoriesView(BrowserView):
    """
    """
    def getCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return self._getCategories(shop)

    def _getCategories(self, obj):
        """
        """        
        categories = []
        
        # TODO: getCategories should return brains
        try:
            obj = obj.getObject()
        except AttributeError:
            pass
            
        for category in ICategoryManagement(obj).getCategories():
            categories.append({
                "title"    : category.Title,
                "uid"      : category.UID,
                "url"      : category.getURL(),
                "children" : self._getCategories(category),
            })
        return categories
                
    def getProducts(self):
        """
        """
        category_uid = self.request.get("category_uid")
        if category_uid is None:
            return []

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = category_uid,
        )
        
        try:
            category = brains[0].getObject()
        except IndexError:
            return []

        line = []
        products = []
        for i, product in enumerate(IProductManagement(category).getProducts()):
            line.append({
                "title" : product.Title(),
                "url"   : product.absolute_url(),
            })
            
            if (i+1) % 5 == 0:
                products.append(line)
                line = []

        if len(line) > 0:
            products.append(line)
        
        return {
            "category_title" : category.Title(),
            "products"       : products,
        }
        
