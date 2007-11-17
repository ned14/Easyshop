# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentMethodValidator

class PaymentValidator(OrderedBaseFolder):
    """An validator to decide whether a customer payment method is valid or 
    not.
    """
    implements(IPaymentMethodValidator)
    _at_rename_after_creation = False
    schema = ATCTMixin.schema.copy()

registerType(PaymentValidator, PROJECTNAME)