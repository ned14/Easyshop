# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IShippingMethod

schema = OrderedBaseFolder.schema.copy()
schema["description"].schemata = "default"

class ShippingMethod(OrderedBaseFolder):
    """A simple shipping method.
    """    
    implements(IShippingMethod)
    _at_rename_after_creation = True
    schema = schema

registerType(ShippingMethod, PROJECTNAME)