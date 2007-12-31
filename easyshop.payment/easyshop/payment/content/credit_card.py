# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import ICreditCardPaymentMethod

# easyshop imports
from easyshop.core.config import PROJECTNAME

class CreditCardPaymentMethod(OrderedBaseFolder):
    """
    """
    implements(ICreditCardPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy()

class CreditCard(BaseContent):
    """Holds all relevant information of a credit cart.
    """
    implements(ICreditCard)

    def Title(self):
        """
        """
        return "%s (%s)" % (self.card_number, self.card_type)

registerType(CreditCardPaymentMethod, PROJECTNAME)        
registerType(CreditCard, PROJECTNAME)