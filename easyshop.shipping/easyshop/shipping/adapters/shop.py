# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import ITaxes
from Products.EasyShop.interfaces import IShippingManagement
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import IShopContent
from Products.EasyShop.content.product.EasyShopProduct import EasyShopProduct


class ShippingManagement:
    """An adapter, which provides shipping management for shop content objects.
    """    
    implements(IShippingManagement)
    adapts(IShopContent)

    def __init__(self, context):
        """
        """
        self.context = context
        self.prices  = self.context.shippingprices
        self.methods = self.context.shippingmethods
        
    def getSelectedShippingMethod(self):
        """
        """
        cm = ICustomerManagement(self.context.getShop())
        customer = cm.getAuthenticatedCustomer()        
        shipping_method_id = customer.getSelectedShippingMethod()
        
        return self.getShippingMethod(shipping_method_id)
        
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
        
        shop = self.context.getShop()
        
        # Todo: By interface
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = ("EasyShopShippingPrice", "DemmelhuberShippingPrice"),
            path = "/".join(self.prices.getPhysicalPath()),
            sort_on = "getObjPositionInParent",
        )

        # Todo: Optimize
        return [brain.getObject() for brain in brains]

    def getShippingMethod(self, id):
        """
        """
        try:
            return self.methods[id]
        except KeyError:
            return None    

    def getShippingMethods(self):
        """
        """
        # Todo: By interface
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = ("EasyShopShippingMethod",),
            path = "/".join(self.methods.getPhysicalPath()),
            sort_on = "getObjPositionInParent",
        )

        # Todo: Optimize
        return [brain.getObject() for brain in brains]

    # Todo: Optimize. The next methods are the same as for pending tax
    # calculations
    def getPriceGross(self):
        """
        """
        for price in self.getShippingPrices():
            if IValidity(price).isValid() == True:
                return price.getPriceGross()
        
        return 0
        
    def getTaxRate(self):
        """
        """
        temp_shipping_product = self.createTemporaryShippingProduct()
        taxes = ITaxes(temp_shipping_product)        
        tax = taxes.getTaxRate()
        return tax

    def getTaxRateForCustomer(self):
        """
        """
        temp_shipping_product = self.createTemporaryShippingProduct()
        taxes = ITaxes(temp_shipping_product)        
        tax = taxes.getTaxRateForCustomer()
        
        return tax

    def getTax(self):
        """
        """
        temp_shipping_product = self.createTemporaryShippingProduct()
        taxes = ITaxes(temp_shipping_product)
        tax = taxes.getTax()
        return tax

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

        taxes = ITaxes(self.context)
        temp_shipping_product = self.createTemporaryShippingProduct()
        tax = taxes.getTaxForCustomer(temp_shipping_product)
        return tax

    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()

    def getPriceForCustomer(self):
        """
        """
        # If there a no items the shipping price is 0        
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()        
        
        if cart is None:
            return 0
                    
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0
        
        return self.getPriceNet() + self.getTaxForCustomer()

    def createTemporaryShippingProduct(self):
        """
        """
        temp_shipping_product = EasyShopProduct("shipping")
        temp_shipping_product.setPriceGross(self.getPriceGross())
        temp_shipping_product.context = self.context
        
        return temp_shipping_product
