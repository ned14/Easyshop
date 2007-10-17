# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IPayPalContent

class EasyShopPayPal(OrderedBaseFolder):
    """Holds all relevant informations for a paypal payment.
    """
    implements(IPayPalContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy()

registerType(EasyShopPayPal, PROJECTNAME)