# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IShippingPriceContent

schema = Schema((

    FloatField(
        name='priceGross',
        widget=DecimalWidget(
            size="10",
            label='Pricegross',
            label_msgid='schema_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

),
)

schema = OrderedBaseFolder.schema.copy() + schema
schema["description"].schemata = "default"
class EasyShopShippingPrice(OrderedBaseFolder):
    """Represents a price for shipping. Has criteria which makes it possible
    for the Shipping manager to calculate a shipping price.
    """    
    implements(IShippingPriceContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = schema

registerType(EasyShopShippingPrice, PROJECTNAME)