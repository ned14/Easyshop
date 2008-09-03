# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IPaymentMethodsContainer
from iqpp.easyshop.interfaces import IPaymentPriceManagementContainer

class PaymentMethodsContainer(OrderedBaseFolder):
    """A simple container to hold payment methods.
    """
    implements(IPaymentMethodsContainer)

class PaymentPricesContainer(OrderedBaseFolder):
    """A simple container to hold payment prices.
    """
    implements(IPaymentPriceManagementContainer)

registerType(PaymentMethodsContainer, PROJECTNAME)
registerType(PaymentPricesContainer, PROJECTNAME)