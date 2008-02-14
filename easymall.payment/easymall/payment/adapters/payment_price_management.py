# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IShop
from easyshop.payment.adapters.payment_price_management \
    import PaymentPriceManagement as BasePaymentPriceManagement

# easymall imports
from easymall.mall.interfaces import IMall

class MallPaymentPriceManagement(BasePaymentPriceManagement):
    """Provides IPaymentPriceManagement for mall content objects.
    """
    implements(IPaymentPriceManagement)
    adapts(IMall)
        
class ShopPaymentPriceManagement(BasePaymentPriceManagement):
    """Provides IPaymentPriceManagement for shop content objects.
    """
    implements(IPaymentPriceManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
        # Get mall
        mall = self.context.aq_inner.aq_parent
        self.paymentprices = mall.paymentprices