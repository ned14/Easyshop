# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShop
from easyshop.catalog.content.product import Product
from easyshop.core.interfaces import IShopManagement

class ShippingPriceManagement(object):
    """An adapter which provides IShippingPriceManagement for shop content objects.
    """    
    implements(IShippingPriceManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.prices  = self.context.shippingprices
        self.methods = self.context.shippingmethods
        
    def getShippingPrice(self, id):
        """
        """        
        try:
            return self.prices[id]
        except KeyError:
            return None
            
    def getShippingPrices(self):
        """
        """
        return self.prices.objectValues()

    def getPriceForCustomer(self):
        """
        """
        # If there a no items the shipping price for cutomers is zero.
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()        
        
        if cart is None:
            return 0
                    
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0
        
        return self.getPriceNet() + self.getTaxForCustomer()

    def getPriceGross(self):
        """
        """
        for price in self.getShippingPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice()
        
        return 0

    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()
        
    def getTaxRate(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTaxRate()

    def getTaxRateForCustomer(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTaxRateForCustomer()

    def getTax(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTax()

    def getTaxForCustomer(self):
        """
        """
        # If there a no items the shipping tax is 0
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()
        
        if cart is None:
            return 0
            
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0

        temp_shipping_product = self._createTemporaryShippingProduct()        
        return ITaxes(temp_shipping_product).getTaxForCustomer()

    def _createTemporaryShippingProduct(self):
        """
        """
        temp_shipping_product = Product("shipping")
        temp_shipping_product.setPrice(self.getPriceGross())
        temp_shipping_product.context = self.context
        
        return temp_shipping_product
