# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import ICompleteness

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