# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.customers.content import Customer
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop
from easyshop.customers.adapters.customer_management \
    import CustomerManagement as BaseCustomerManagement

# easymall imports    
from easymall.mall.interfaces import IMall

class MallCustomerManagement(BaseCustomerManagement):
    """Provides customer management for mall content objects.
    """
    implements(ICustomerManagement)
    adapts(IMall)

class ShopCustomerManagement(BaseCustomerManagement):
    """Provides customer management for shop content objects.
    """
    implements(ICustomerManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
        # Get mall
        mall = self.context.aq_inner.aq_parent
        self.customers = mall.customers
        self.sessions  = mall.sessions