# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# plone imports
from plone.app.content.item import Item

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IDirectDebit

class DirectDebit(Item):
    """Holds all relevant informations for direct debit payment method. This is 
    a bank account.
    """
    implements(IDirectDebit)
    portal_type = "DirectDebit"
    
    account_number = FieldProperty(IDirectDebit["account_number"])
    bank_identification_code = FieldProperty(IDirectDebit["bank_identification_code"])
    bank_name = FieldProperty(IDirectDebit["bank_name"])
    depositor = FieldProperty(IDirectDebit["depositor"])

    def Title(self):
        """
        """
        return self.bank_name + " - " + self.account_number
        
directDebitFactory = Factory(DirectDebit, title=_(u"Create a new direct debit"))