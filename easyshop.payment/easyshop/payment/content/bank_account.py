# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# plone imports
from plone.app.content.item import Item

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IBankAccount

class BankAccount(Item):
    """Holds all relevant informations for direct debit payment method. This is 
    a bank account.
    """
    implements(IBankAccount)
    portal_type = "BankAccount"
    
    account_number = FieldProperty(IBankAccount["account_number"])
    bank_identification_code = FieldProperty(IBankAccount["bank_identification_code"])
    bank_name = FieldProperty(IBankAccount["bank_name"])
    depositor = FieldProperty(IBankAccount["depositor"])

    def Title(self):
        """
        """
        return self.bank_name + " - " + self.account_number
        
bankAccountFactory = Factory(BankAccount, title=_(u"Create a new bank account"))       
