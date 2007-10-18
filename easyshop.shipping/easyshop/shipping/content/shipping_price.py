# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IShippingPrice
from Products.EasyShop.interfaces import IShippingPricesContainer

from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement

class ShippingPriceBase(BaseFolder):
    """The base class for shipping prices. Developer may inherit from it, to 
    write own shipping prices.
    """
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


schema = Schema((

    FloatField(
        name='priceGross',
        widget=DecimalWidget(
            size="10",
            label='Pricegross',
            label_msgid='schema_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

),
)
schema = OrderedBaseFolder.schema.copy() + schema
schema["description"].schemata = "default"
class ShippingPrice(OrderedBaseFolder):
    """Represents a price for shipping. Has criteria which makes it possible
    for the Shipping manager to calculate a shipping price.
    """    
    implements(IShippingPrice)    
    schema = schema

class ShippingPricesContainer(OrderedBaseFolder):
    """A simple container to hold shipping prices.
    """
    implements(IShippingPricesContainer)
                  
registerType(ShippingPricesContainer, PROJECTNAME)
registerType(ShippingPrice, PROJECTNAME)