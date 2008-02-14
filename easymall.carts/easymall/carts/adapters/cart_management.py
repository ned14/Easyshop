# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IShop
from easyshop.carts.adapters.cart_management \
    import CartManagement as BaseCartManagement

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

class MallCartManagement(BaseCartManagement):
    """Adapter which provides ICartManagement for mall content objects.
    """
    implements(ICartManagement)
    adapts(IMall)