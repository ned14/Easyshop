# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IValidity

from easyshop.shipping.adapters.shipping_price_management \
    import ShippingPriceManagement as BaseShippingPriceManagement

# easymall imports    
from easymall.mall.interfaces import IMall

class MallShippingPriceManagement(BaseShippingPriceManagement):
    """An adapter which provides IShippingPriceManagement for mall content objects.
    """    
    implements(IShippingPriceManagement)
    adapts(IMall)

    def getPriceGross(self):
        """
        """
        amount_of_shops = ICartManagement(self.context).getAmountOfShops()
        
        for price in self.getShippingPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice() * amount_of_shops
        
        return 0
        
class ShopShippingPriceManagement(BaseShippingPriceManagement):
    """An adapter which provides IShippingPriceManagement for shop content objects.
    """    
    implements(IShippingPriceManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
        mall = self.context.aq_inner.aq_parent
        self.prices  = mall.shippingprices
        self.methods = mall.shippingmethods
        
    def getPriceGross(self):
        """
        """
        amount_of_shops = ICartManagement(self.context).getAmountOfShops()
        
        for price in self.getShippingPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice() * amount_of_shops
        
        return 0