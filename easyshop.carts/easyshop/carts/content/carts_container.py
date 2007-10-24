# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.carts.config import *
from easyshop.core.interfaces.carts import ICartsContainer

class CartsContainer(BaseBTreeFolder):
    """A simple container to hold carts.
    """
    implements(ICartsContainer)
    
registerType(CartsContainer, PROJECTNAME)