# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop import
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShop
from easyshop.order.adapters.order_management \
    import OrderManagement as BaseOrderManagement

# easymall imports
from easymall.mall.interfaces import IMall

class MallOrderManagement(BaseOrderManagement):
    """An adapter, which provides order management for mall content objects.
    """
    implements(IOrderManagement)
    adapts(IMall)

class ShopOrderManagement(BaseOrderManagement):
    """An adapter, which provides order management for shop content objects.
    """
    implements(IOrderManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
        # Get mall
        mall = self.context.aq_inner.aq_parent
        self.orders = mall.orders