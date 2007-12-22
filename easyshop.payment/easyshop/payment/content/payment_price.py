# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentPrice

schema = Schema((

    TextField(
        'description',
        default='',
        searchable=1,
        accessor="Description",
        widget=TextAreaWidget(
            label='Description',
            description="A short summary of the content",
            label_msgid="label_description",
            description_msgid="help_description",
            i18n_domain="plone"),
    ),
    
    FloatField(
        name="price",
        required=True,
        widget=DecimalWidget(
            size="10",
            label="Price",
            label_msgid="schema_price_label",
            i18n_domain="EasyShop",
        )
    ),

),
)

class PaymentPrice(OrderedBaseFolder):
    """Represents a price for payment methods. Has criteria which makes it
    possible for the payment manager to calculate a payment price.
    """
    implements(IPaymentPrice)

    _at_rename_after_creation = True
    schema = BaseFolderSchema.copy() + schema.copy()

registerType(PaymentPrice, PROJECTNAME)