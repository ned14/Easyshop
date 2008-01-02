# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IBankAccount

class BankAccount(BaseContent):
    """Holds all relevant informations for direct debit payment method. This is 
    a bank account.
    """    
    implements(IBankAccount)
    
    def Title(self):
        """
        """
        return self.bank_name + " - " + self.account_number
        
registerType(BankAccount, PROJECTNAME)
