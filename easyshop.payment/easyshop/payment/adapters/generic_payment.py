# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import IGenericPaymentMethod

from easyshop.payment.content import PaymentResult
from easyshop.payment.config import NOT_PAYED
from easyshop.payment.config import PAYED

class GenericPaymentType:
    """Provides IType for simple payment content objects.
    """
    implements(IType)
    adapts(IGenericPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type.
        """
        return "generic-payment"
        

class GenericPaymentCompleteness:
    """Provides ICompleteness for simple payment content objects.
    """
    implements(ICompleteness)
    adapts(IGenericPaymentMethod)
    
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns always true, as generic payment method needs no informations.
        """        
        return True        
        
class GenericPaymentProcessor:
    """Provides IPaymentProcessing for simple payment content objects.
    """
    implements(IPaymentProcessing)
    adapts(IGenericPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        if self.context.getPayed() == True:
            code = PAYED
        else:
            code = NOT_PAYED
            
        return PaymentResult(code, "")