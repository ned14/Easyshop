# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class ProductRelatedProductsView(BrowserView):
    """
    """
    def hasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.hasPhotos()

    def getPriceForCustomer(self):
        """
        """
        p = IPrices(self.context)
        price = p.getPriceForCustomer()
        
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)
        
    def getMainPhoto(self):
        """
        """   
        pm = IPhotoManagement(self.context)
        return pm.getMainPhoto()

    def getProduct(self):
        """
        """
        data = IData(self.context)
        return data.asDict()
        
    def getRelatedProducts(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs('easyshopproduct_easyshopproducts'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result

    def getShowAddQuantity(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return shop.getShowAddQuantity()

    def showSelectPropertiesView(self):
        """
        """
        property_manager = IPropertyManagement(self.context)
                
        if len(property_manager.getProperties()) > 0:
            return True

        return False        