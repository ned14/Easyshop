# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import IDirectDebit

from easyshop.payment.content import PaymentResult
from easyshop.payment.config import NOT_PAYED

class DirectDebitType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(IDirectDebit)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of EasyShopDirectDebit.
        """
        return "direct-debit"
        

class DirectDebitPaymentProcessor:
    """Provides IPaymentProcessing for direct debit content objects.
    """
    implements(IPaymentProcessing)
    adapts(IDirectDebit)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """        
        return PaymentResult("NOT_PAYED", "")
        
class DirectDebitCompleteness:
    """Provides ICompleteness for direct debit content objects.
    """    
    implements(ICompleteness)
    adapts(IDirectDebit)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the direct debit informations are complete.
        """        
        if len(self.context.account_number) == 0:
            return False
        elif len(self.context.bank_identification_code) == 0:
            return False
        elif len(self.context.depositor) == 0:
            return False
        elif len(self.context.bank_name) == 0:
            return False

        return True