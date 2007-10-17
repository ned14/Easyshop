# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IDirectDebitContent

schema = Schema((

    StringField(
        name='accountNumber',
        required=1,
        widget=StringWidget(
            label='Account Number',
            label_msgid='schema_account_number_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='bankIdentificationCode',
        required=1,        
        widget=StringWidget(
            label='Bank Identification Code',
            label_msgid='schema_bank_identification_code_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='name',
        required=1,        
        widget=StringWidget(
            label='Name',
            label_msgid='schema_name_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='bankName',
        required=1,
        widget=StringWidget(
            label='Bankname',
            label_msgid='schema_bankname_label',
            i18n_domain='EasyShop',
        )
    ),

),
)

EasyShopDirectDebit_schema = BaseSchema.copy() + schema.copy()
EasyShopDirectDebit_schema["title"].widget.visible = {'view':'invisible', 'edit':'invisible'}
EasyShopDirectDebit_schema["title"].required = 0

class EasyShopDirectDebit(OrderedBaseFolder):
    """Holds all relevant informations for a direct debit payment. 
    """
    implements(IDirectDebitContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = EasyShopDirectDebit_schema

    def Title(self):
        """
        """
        return self.getAccountNumber()

registerType(EasyShopDirectDebit, PROJECTNAME)