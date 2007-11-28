# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.payment.config import NOT_PAYED
from easyshop.payment.content import PaymentResult
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IDirectDebitPaymentMethod
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import IShopManagement

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
        

class DirectDebitPaymentProcessor:
    """Provides IPaymentProcessing for direct debit payment method.
    """
    implements(IPaymentProcessing)
    adapts(IDirectDebitPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """        
        return PaymentResult(NOT_PAYED, "")


class DirectDebitPaymentMethodCompleteness:
    """Provides ICompleteness for direct debit payment method.
    """    
    implements(ICompleteness)
    adapts(IDirectDebitPaymentMethod)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """
        """
        shop         = IShopManagement(self.context).getShop()
        customer     = ICustomerManagement(shop).getAuthenticatedCustomer()        
        pim          = IPaymentInformationManagement(customer)
        bank_account = pim.getSelectedPaymentInformation()
        
        if IBankAccount.providedBy(bank_account) == False or \
           ICompleteness(bank_account) == False:
            return False
        else:        
            return True