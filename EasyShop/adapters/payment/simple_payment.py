# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICompleteness
from Products.EasyShop.interfaces import IPaymentProcessing
from Products.EasyShop.interfaces import IType
from Products.EasyShop.interfaces import ISimplePaymentMethodContent

class SimplePaymentType:
    """Provides IType for simple payment content objects.
    """
    implements(IType)
    adapts(ISimplePaymentMethodContent)

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
    adapts(ISimplePaymentMethodContent)
    
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
    adapts(ISimplePaymentMethodContent)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        if self.context.getPayed() == True:
            return "PAYED"
        else:
            return "NOT_PAYED"