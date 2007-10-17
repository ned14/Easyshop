# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import ITaxContent

schema = Schema((

    FloatField(
        name='rate',
        widget=DecimalWidget(
            label='Rate',
            label_msgid='schema_rate_label',
            i18n_domain='EasyShop',
        )
    ),

),
)

class EasyShopCustomerTax(OrderedBaseFolder):
    """Represents taxes for customers.
    
    This is used to calculate the price for the customer on base of the net
    price.
    
    It is able to hold criteria which let the tax manager decide which tax is
    taken for a customer / product / category / group / date / ...
    """
    implements(ITaxContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = OrderedBaseFolderSchema.copy() + schema.copy()

registerType(EasyShopCustomerTax, PROJECTNAME)