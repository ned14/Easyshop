# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IGenericPaymentMethod

schema = Schema((
    BooleanField(
        name = "payed",
        languageIndependent=True,
        widget = BooleanWidget(
            label="Payed",
            label_msgid="schema_payment_state_label",
            description = "If checked, the order state will set to payed.",
            description_msgid="schema_payment_state_description",
            i18n_domain="EasyShop",
        ),
    ),        
),
)

schema = ATCTMixin.schema.copy() + schema.copy()
schema["title"].required = False

class GenericPaymentMethod(OrderedBaseFolder):
    """A generic payment method.
    """
    implements(IGenericPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = schema

registerType(GenericPaymentMethod, PROJECTNAME)