# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IPaymentMethodValidatorContent

class EasyShopPaymentValidator(OrderedBaseFolder):
    """An validator to decide whether a customer payment method is valid or 
    not.
    """
    implements(IPaymentMethodValidatorContent)
    _at_rename_after_creation = False
    schema = ATCTMixin.schema.copy()

registerType(EasyShopPaymentValidator, PROJECTNAME)