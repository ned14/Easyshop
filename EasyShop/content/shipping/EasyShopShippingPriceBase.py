# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IShippingPriceContent
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IProductManagement

class EasyShopShippingPriceBase(BaseFolder):
    """The base class for shipping prices. 
    
    Developer may inherit from it, to write own shipping prices.
    """    
    implements(IShippingPriceContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True    
    schema = BaseFolderSchema.copy()
    
    def getCart(self):
        """Provides the cart of authenticated customer.
        """        
        shop = self.getShop()
        return ICartManagement(shop).getCart()
            
    def getCartItems(self):
        """Provides the cart items.
        """
        cart = self.getCart()    
        return IItemManagement(cart).getItems()
