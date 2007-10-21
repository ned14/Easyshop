# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IData
from Products.EasyShop.interfaces import IPhotoManagement
from Products.EasyShop.interfaces import IPropertyManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IShopManagement

class IProductRelatedProductsView(Interface):    
    """
    """
    def hasPhotos():
        """
        """

    def getPriceForCustomer():
        """
        """    
        
    def getMainPhoto():
        """
        """   

    def getProduct():
        """
        """
        
    def getRelatedProducts():
        """
        """

    def getShowAddQuantity():
        """
        """        

    def showSelectPropertiesView():
        """
        """
        
class ProductRelatedProductsView(BrowserView):
    """
    """
    implements(IProductRelatedProductsView)
    
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