# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IPaymentMethodsContainer
from Products.EasyShop.interfaces import IPaymentPricesContainer

class PaymentMethodsContainer(OrderedBaseFolder):
    """A simple container to hold payment methods.
    """
    implements(IPaymentMethodsContainer)

class PaymentPricesContainer(OrderedBaseFolder):
    """A simple container to hold payment prices.
    """
    implements(IPaymentPricesContainer)

registerType(PaymentMethodsContainer, PROJECTNAME)
registerType(PaymentPricesContainer, PROJECTNAME)