# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType

class CreditCardType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(ICreditCard)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of CreditCard.
        """
        return "credit-card"
        

class CreditCardPaymentProcessor:
    """Provides IPaymentProcessing for direct debit content objects.
    """
    implements(IPaymentProcessing)
    adapts(ICreditCard)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        return "PAYED"
        
class CreditCardCompleteness:
    """Provides ICompleteness for direct debit content objects.
    """    
    implements(ICompleteness)
    adapts(ICreditCard)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the direct debit informations are complete.
        """        
        return True