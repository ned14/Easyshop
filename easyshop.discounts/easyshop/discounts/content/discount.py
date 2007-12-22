# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IDiscount

schema = Schema((

    FloatField(
        name='value',
        widget=DecimalWidget(
            label='Value',
            label_msgid='schema_value_label',
            description='The discount which is given.',
            description_msgid='schema_value_description',
            i18n_domain='EasyShop',
        )
    ),

),
)

class Discount(OrderedBaseFolder):
    """A discount on cart price.
    """
    implements(IDiscount)
    _at_rename_after_creation = True
    schema = OrderedBaseFolderSchema.copy() + schema.copy()

registerType(Discount, PROJECTNAME)