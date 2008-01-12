# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IShippingPrice

from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement

class ShippingPriceBase(OrderedBaseFolder):
    """The base class for shipping prices. Developer may inherit from it, to 
    write own shipping prices.
    """
    security = ClassSecurityInfo()
    _at_rename_after_creation = True    
    schema = BaseFolderSchema.copy()
    
    def getCart(self):
        """Provides the cart of authenticated customer.
        """        
        shop = IShopManagement(self).getShop()
        return ICartManagement(shop).getCart()
            
    def getCartItems(self):
        """Provides the cart items.
        """
        cart = self.getCart()    
        return IItemManagement(cart).getItems()


schema = Schema((

    FloatField(
        name='price',
        widget=DecimalWidget(
            size="10",
            label='Price',
            label_msgid='schema_price_label',
            i18n_domain='EasyShop',
        )
    ),

),
)

schema = OrderedBaseFolder.schema.copy() + schema
schema["description"].schemata = "default"

class ShippingPrice(ShippingPriceBase):
    """Represents a price for shipping. Has criteria which makes it possible
    for the Shipping manager to calculate a shipping price.
    """    
    implements(IShippingPrice)    
    schema = schema

registerType(ShippingPrice, PROJECTNAME)