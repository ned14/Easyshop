# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShop
from easyshop.shipping.adapters.shipping_method_management \
    import ShippingMethodManagement as BaseShippingMethodManagement

# easymall imports    
from easymall.mall.interfaces import IMall

class MallShippingMethodManagement(BaseShippingMethodManagement):
    """An adapter which provides IShippingMethodManagement for shop content 
    objects.
    """    
    implements(IShippingMethodManagement)
    adapts(IMall)

class ShopShippingMethodManagement(BaseShippingMethodManagement):
    """An adapter which provides IShippingMethodManagement for shop content 
    objects.
    """    
    implements(IShippingMethodManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

        # Shipping methods are taken out of the mall not the shop anymore.
        mall = self.context.aq_inner.aq_parent
        self.shipping_methods = mall.shippingmethods