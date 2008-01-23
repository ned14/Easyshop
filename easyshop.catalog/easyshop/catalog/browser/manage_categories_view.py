# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class ManageCategoriesView(BrowserView):
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
        
        try:
            obj = obj.getObject()
        except AttributeError:
            pass
            
        for category in ICategoryManagement(obj).getTopLevelCategories():
            
            if category.UID == self.context.UID():
                klass = "current-category"
            else:
                klass = ""
                
            categories.append({
                "title"    : category.Title,
                "uid"      : category.UID,
                "url"      : category.getURL(),
                "children" : self._getCategories(category),
                "class"    : klass,
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
        for i, product in enumerate(IProductManagement(category).getAllProducts()):
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
            "category_title"       : category.Title(),
            "category_description" : category.Description(),
            "products"             : products,
        }