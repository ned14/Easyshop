# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IBankAccount

schema = Schema((

    StringField(
        name='account_number',
        required=1,
        widget=StringWidget(
            label='Account Number',
            label_msgid='schema_account_number_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='bank_identification_code',
        required=1,        
        widget=StringWidget(
            label='Bank Identification Code',
            label_msgid='schema_bank_identification_code_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='depositor',
        required=1,        
        widget=StringWidget(
            label='Depositor',
            label_msgid='schema_name_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='bank_name',
        required=1,
        widget=StringWidget(
            label='Bankname',
            label_msgid='schema_bankname_label',
            i18n_domain='EasyShop',
        )
    ),

),
)

class BankAccount(BaseContent):
    """Holds all relevant informations for direct debit payment method. This is 
    a bank account.
    """    
    implements(IBankAccount)
    schema = schema
    
    def Title(self):
        """
        """
        return self.bank_name + " - " + self.account_number
        
registerType(BankAccount, PROJECTNAME)
