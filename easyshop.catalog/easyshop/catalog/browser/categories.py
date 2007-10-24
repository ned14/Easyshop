# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShopManagement

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