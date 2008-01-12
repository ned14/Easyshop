# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICreditCardPaymentMethod
from easyshop.core.interfaces import IDirectDebitPaymentMethod
from easyshop.core.interfaces import IGenericPaymentMethod
from easyshop.core.interfaces import IPayPalPaymentMethod
from easyshop.core.interfaces import IType

class CreditCardType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of credit card payment method.
        """
        return "credit-card"

class DirectDebitType:
    """Provides IType for direct debit payment method.
    """
    implements(IType)
    adapts(IDirectDebitPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of direct debit payment method.
        """
        return "direct-debit"

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
                        
class PayPalType:
    """Provides IType for paypal content objects.
    """
    implements(IType)
    adapts(IPayPalPaymentMethod)

    def __init__(self, context):
        self.context = context                  

    def getType(self):
        """Returns type of EasyShopPrepayment.
        """
        return "paypal"        