# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IPayPalPaymentMethod

class PayPalPaymentMethod(OrderedBaseFolder):
    """Holds all relevant informations for a paypal payment.
    """
    implements(IPayPalPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy()

registerType(PayPalPaymentMethod, PROJECTNAME)

