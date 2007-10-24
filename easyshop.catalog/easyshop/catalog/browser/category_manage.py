# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class CategoryManageView(BrowserView):
    """
    """
    def getProducts(self):
        """Returns direct products (no products of sub categories) of a
        category.
        """
        result = []
        pm = IProductManagement(self.context)
        for product in pm.getProducts():

            photo = IPhotoManagement(product).getMainPhoto()
            if photo is not None:
                image = "%s/image_%s" % (photo.absolute_url(), "thumb")
            else:
                image = None
            
            result.append({
                "title" : product.getShortTitle() or product.Title(),
                "url"   : product.absolute_url(),
                "image" : image,
            })
            
        return result
        
    def getTopLevelCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        cm   = ICategoryManagement(shop)
        
        result = []
        for category in cm.getTopLevelCategories():
                  
            result.append({
                "title"       : category.Title,
                "description" : category.Description,
                "url"         : "%s/manage" % category.getURL()
            })
            
        return result