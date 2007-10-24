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
from easyshop.core.interfaces import IPayPal

class PayPal(OrderedBaseFolder):
    """Holds all relevant informations for a paypal payment.
    """
    implements(IPayPal)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy()

registerType(PayPal, PROJECTNAME)