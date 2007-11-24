# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# plone imports
from plone.app.content.item import Item

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IDirectDebitPaymentMethod

# easyshop imports
from easyshop.core.config import PROJECTNAME

class DirectDebitPaymentMethod(OrderedBaseFolder):
    """
    """
    implements(IDirectDebitPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy()

registerType(DirectDebitPaymentMethod, PROJECTNAME) 