# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICompleteness
from Products.EasyShop.interfaces import IPaymentProcessing
from Products.EasyShop.interfaces import IType
from Products.EasyShop.interfaces import IDirectDebitContent

class DirectDebitType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(IDirectDebitContent)

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
    adapts(IDirectDebitContent)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        return "NOT_PAYED"
        
class DirectDebitCompleteness:
    """Provides ICompleteness for direct debit content objects.
    """    
    implements(ICompleteness)
    adapts(IDirectDebitContent)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the direct debit informations are complete.
        """        
        if len(self.context.getAccountNumber()) == 0:
            return False
        elif len(self.context.getBankIdentificationCode()) == 0:
            return False
        elif len(self.context.getName()) == 0:
            return False
        elif len(self.context.getBankName()) == 0:
            return False

        return True