# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import ISimplePaymentMethod

from easyshop.payment.config import PAYED, NOT_PAYED
from easyshop.payment.content import PaymentResult

class SimplePaymentType:
    """Provides IType for simple payment content objects.
    """
    implements(IType)
    adapts(ISimplePaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of EasyShopPrepayment.
        """
        return "simple-payment"
        

class SimplePaymentCompleteness:
    """Provides ICompleteness for simple payment content objects.
    """
    implements(ICompleteness)
    adapts(ISimplePaymentMethod)
    
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns always true, as prepayment needs no informations.
        """        
        return True        
        
class SimplePaymentProcessor:
    """Provides IPaymentProcessing for simple payment content objects.
    """
    implements(IPaymentProcessing)
    adapts(ISimplePaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        if self.context.getPayed() == True:
            code = "PAYED"
        else:
            code = "NOT_PAYED"
            
        PaymentResult(code, "")