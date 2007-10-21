# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import ICategoryManagement
from Products.EasyShop.interfaces import IShopManagement

class CategoriesView(BrowserView):
    """
    """
    def getTopLevelCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        
        cm = ICategoryManagement(shop)
        
        result = []
        for category in cm.getTopLevelCategories():
            result.append({
                "title"       : category.Title,
                "description" : category.Description,
                "url"         : category.getURL(),
            })
            
        return result