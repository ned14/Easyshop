# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.content.shipping.EasyShopShippingPriceBase import EasyShopShippingPriceBase
from Products.EasyShop.interfaces import IShippingPriceContent
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IGroupManagement
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IAddressManagement

SPEDITION = {
    50  : 29.9,
    100 : 32.9,
    150 : 39.9,
    200 : 49.9,
    250 : 59.9,
    300 : 69.9,
    350 : 79.9,
    400 : 89.9,
}

POST = {
    5  : 7.0,
    10 : 10.5,
    20 : 14.0,
    25 : 21.0,
    30 : 24.5,
    40 : 28.0,
    45 : 35.0,
    50 : 38.5,
    60 : 42.0,
}

class DemmelhuberShippingPrice(EasyShopShippingPriceBase):
    """Represents a special shipping price for demmelhuber.
    """    
    implements(IShippingPriceContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True    
    schema = BaseFolderSchema.copy()
    
    security.declarePublic("getPriceGross")
    def getPriceGross(self):
        """
        """
        shop = self.getShop()
        cm = ICustomerManagement(shop)
        customer = cm.getAuthenticatedCustomer()

        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        if address is None:
            return 0.0

        try:    
            if address.getCountry() != "Deutschland":
                return 0.0
        except:
            return 0.0
            
        cart_weight = 0
        kindof_shipping = POST
        for item in self.getCartItems():            
            groups = IGroupManagement(item.getProduct()).getGroups()
            groups = [group.getId() for group in groups]
            if "versand-spedition" in groups:
                kindof_shipping = SPEDITION
            try:
                cart_weight += item.getProduct().getWeight() * item.getAmount()
            except AttributeError:
                return 0.0
        
        limits = kindof_shipping.keys()
        limits.sort()

        found = limits[0]
        for limit in limits:
            if cart_weight < limit:
                break
            found = limit

        return kindof_shipping[found]
                
registerType(DemmelhuberShippingPrice, PROJECTNAME)