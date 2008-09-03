# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from iqpp.easyshop.interfaces import IBankAccount
from iqpp.easyshop.interfaces import ICompleteness
from iqpp.easyshop.interfaces import ICreditCard
from iqpp.easyshop.interfaces import ICreditCardPaymentMethod
from iqpp.easyshop.interfaces import ICustomerManagement
from iqpp.easyshop.interfaces import IDirectDebitPaymentMethod
from iqpp.easyshop.interfaces import IGenericPaymentMethod
from iqpp.easyshop.interfaces import IPaymentInformationManagement
from iqpp.easyshop.interfaces import IPayPalPaymentMethod
from iqpp.easyshop.interfaces import IShopManagement

class BankAccountCompleteness:
    """Provides ICompleteness for bank account content objects.
    """    
    implements(ICompleteness)
    adapts(IBankAccount)
        
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
        """Returns true if the credit card informations are complete.
        """        
        return True        
                
class CreditCardPaymentMethodCompleteness:
    """
    """
    implements(ICompleteness)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the credit card informations are complete.
        """        
        return True

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

class GenericPaymentCompleteness:
    """Provides ICompleteness for generic payment content objects.
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
                    
class PayPalCompleteness:
    """Provides ICompleteness for paypal content objects.
    """
    implements(ICompleteness)
    adapts(IPayPalPaymentMethod)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """For PayPal no information is needed
        """        
        return True