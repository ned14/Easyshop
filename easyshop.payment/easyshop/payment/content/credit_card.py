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

class CreditCard(Item):
    """Holds all relevant information of a credit cart.
    """
    implements(ICreditCard)
    portal_type = "CreditCard"

    card_type                  = FieldProperty(ICreditCard["card_type"])
    card_owner                 = FieldProperty(ICreditCard["card_owner"])
    card_number                = FieldProperty(ICreditCard["card_number"])
    card_expiration_date_month = FieldProperty(ICreditCard["card_expiration_date_month"])
    card_expiration_date_year  = FieldProperty(ICreditCard["card_expiration_date_year"])
        
    def Title(self):
        """
        """
        return "%s (%s)" % (self.card_number, self.card_type)

registerType(CreditCardPaymentMethod, PROJECTNAME)        
creditCardFactory = Factory(CreditCard, title=_(u"Create a new credit card."))