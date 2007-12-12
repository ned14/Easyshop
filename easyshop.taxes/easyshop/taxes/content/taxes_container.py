# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import ITaxesContainer

class TaxesContainer(OrderedBaseFolder):
    """A simple container to hold taxes.
    """
    implements(ITaxesContainer)

registerType(TaxesContainer, PROJECTNAME)