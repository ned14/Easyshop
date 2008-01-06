# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import IValidity
from easyshop.nochex.interfaces import INochexPaymentMethod
from easyshop.payment.config import NOT_PAYED
from easyshop.payment.content import PaymentResult
from easyshop.shop.adapters.validity import Validity

NOCHEX_URL = "https://secure.nochex.com"
NOCHEX_ID  = "public0815@gmx.net"

class NochexPaymentProcessor:
    """Provides IPaymentProcessing for Nochex content objects.
    """
    implements(IPaymentProcessing)
    adapts(INochexPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def process(self, order=None):
        """
        """    
        shop = IShopManagement(self.context).getShop()                        
        notify_url = "%s/paypal?order=%s" % (shop.absolute_url(), order.UID())
        return_url = "%s/thank-you" % shop.absolute_url()
        
        pc = IPrices(order)
        price_gross = "%.2f" % pc.getPriceGross()
        
        info = {
            "merchant_id" : NOCHEX_ID,
            "amount" : price_gross,
            "order_id": order.getId(),
        }

        # redirect to paypal    
        parameters = "&".join(["%s=%s" % (k, v) for (k, v) in info.items()])                
        
        url = NOCHEX_URL + "?" + parameters
        self.context.REQUEST.RESPONSE.redirect(url)
        
        return PaymentResult(NOT_PAYED)
        
class NochexValidity(Validity):
    """An adapter which provides IValidity for Nochex payment method.
    """
    implements(IValidity)
    adapts(INochexPaymentMethod)
     
    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns False if the Nochex id is not filled in.
        """
        # shop = IShopManagement(self.context).getShop()
        # if shop.getPayPalId() == "":
        #     return False

        return super(NochexValidity, self).isValid(product)
        
class NochexCompleteness:
    """Provides ICompleteness for Nochex content objects.
    """
    implements(ICompleteness)
    adapts(INochexPaymentMethod)
        
    def __init__(self, context):
        """
        """
        self.context = context

    def isComplete(self):
        """For Nochex no information is needed.
        """        
        return True        
        
class NochexType:
    """Provides IType for paypal content objects.
    """
    implements(IType)
    adapts(INochexPaymentMethod)

    def __init__(self, context):
        self.context = context                  

    def getType(self):
        """Returns type of Nochex.
        """
        return "nochex"