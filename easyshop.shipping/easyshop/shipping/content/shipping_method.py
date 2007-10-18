# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IShippingMethod
from Products.EasyShop.interfaces import IShippingMethodsContainer

schema = OrderedBaseFolder.schema.copy()
schema["description"].schemata = "default"

class ShippingMethod(OrderedBaseFolder):
    """A simple shipping method.
    """    
    implements(IShippingMethod)
    _at_rename_after_creation = True
    schema = schema

class ShippingMethodsContainer(OrderedBaseFolder):
    """A simple container to hold shipping methods.
    """
    implements(IShippingMethodsContainer)

registerType(ShippingMethodsContainer, PROJECTNAME)
registerType(ShippingMethod, PROJECTNAME)