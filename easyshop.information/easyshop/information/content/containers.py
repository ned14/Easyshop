# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IInformationContainer

class InformationContainer(OrderedBaseFolder):
    """A simple container to hold information like terms and conditions.
    """    
    implements(IInformationContainer)

registerType(InformationContainer, PROJECTNAME)