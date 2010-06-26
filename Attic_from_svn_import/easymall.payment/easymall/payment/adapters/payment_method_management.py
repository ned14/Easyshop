# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IShop
from easyshop.payment.adapters.payment_method_management \
    import PaymentMethodManagement as BasePaymentMethodManagement

# easymall imports
from easymall.mall.interfaces import IMall

class MallPaymentMethodManagement(BasePaymentMethodManagement):
    """An adapter which provides IPaymentMethodManagement for mall content
    objects.
    """
    implements(IPaymentMethodManagement)
    adapts(IMall)

class ShopPaymentMethodManagement(BasePaymentMethodManagement):
    """An adapter which provides IPaymentMethodManagement for shop content
    objects.
    """
    implements(IPaymentMethodManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        
        # Get mall
        mall = self.context.aq_inner.aq_parent
        self.paymentmethods = mall.paymentmethods