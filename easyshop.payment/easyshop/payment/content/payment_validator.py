# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IPaymentMethodValidator

class PaymentValidator(OrderedBaseFolder):
    """An validator to decide whether a customer payment method is valid or 
    not.
    """
    implements(IPaymentMethodValidator)
    _at_rename_after_creation = False
    schema = ATCTMixin.schema.copy()

registerType(PaymentValidator, PROJECTNAME)