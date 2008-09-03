# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IShippingMethodsContainer
from iqpp.easyshop.interfaces import IShippingPricesContainer

class ShippingPricesContainer(OrderedBaseFolder):
    """A simple container to hold shipping prices.
    """
    implements(IShippingPricesContainer)
                  

class ShippingMethodsContainer(OrderedBaseFolder):
    """A simple container to hold shipping methods.
    """
    implements(IShippingMethodsContainer)

registerType(ShippingPricesContainer, PROJECTNAME)
registerType(ShippingMethodsContainer, PROJECTNAME)