# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import ITaxesContainer

class TaxesContainer(OrderedBaseFolder):
    """A simple container to hold taxes.
    """
    implements(ITaxesContainer)

registerType(TaxesContainer, PROJECTNAME)