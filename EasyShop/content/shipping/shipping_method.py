# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IShippingMethodContent

schema = OrderedBaseFolder.schema.copy()
schema["description"].schemata = "default"
class EasyShopShippingMethod(OrderedBaseFolder):
    """A simple shipping method.
    """    
    implements(IShippingMethodContent)
    _at_rename_after_creation = True
    schema = schema
        
registerType(EasyShopShippingMethod, PROJECTNAME)