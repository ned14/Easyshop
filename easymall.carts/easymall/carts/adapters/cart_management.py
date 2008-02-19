# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.carts.adapters.cart_management \
    import CartManagement as BaseCartManagement

from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

# easymall imports
from easymall.mall.interfaces import IMall

class ShopCartManagement(BaseCartManagement):
    """Adapter which provides ICartManagement for shop content objects.
    """
    implements(ICartManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """        
        self.context = context
        
        # All carts are taken from the mall not the shop anymore
        mall = self.context.aq_inner.aq_parent
        self.carts = mall.carts

    def getAmountOfShops(self):
        """
        """
        cart = self.getCart()
        
        shops = {}
        for item in IItemManagement(cart).getItems():
            shop = IShopManagement(item.getProduct()).getShop()
            shops[shop.UID()] = 1
            
        return len(shops.keys())
        
class MallCartManagement(BaseCartManagement):
    """Adapter which provides ICartManagement for mall content objects.
    """
    implements(ICartManagement)
    adapts(IMall)
    
    def getAmountOfShops(self):
        """
        """
        cart = self.getCart()
        
        shops = {}
        for item in IItemManagement(cart).getItems():
            shop = IShopManagement(item.getProduct()).getShop()
            shops[shop.UID()] = 1
            
        return len(shops.keys())