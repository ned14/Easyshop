# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentPrice

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

class PaymentPrice(OrderedBaseFolder):
    """Represents a price for payment methods. Has criteria which makes it
    possible for the payment manager to calculate a payment price.
    """
    implements(IPaymentPrice)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseFolderSchema.copy() + schema.copy()

registerType(PaymentPrice, PROJECTNAME)