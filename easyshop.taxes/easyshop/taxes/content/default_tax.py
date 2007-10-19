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

class DefaultTax(OrderedBaseFolder):
    """Represents taxes, which are common for the country in which the shop is
    running. 
       
    This is used to calculate the net price on base of the entered gross 
    price. The gross price is the base price for all further calculations.
              
    It is able to hold criteria which let the tax manager decide  which tax is 
    taken for a product / category / group / ...
    """
    implements(ITaxContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = OrderedBaseFolderSchema.copy() + schema.copy()

registerType(DefaultTax, PROJECTNAME)