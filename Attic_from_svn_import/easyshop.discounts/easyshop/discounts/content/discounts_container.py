# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IDiscountsContainer

class DiscountsContainer(OrderedBaseFolder):
    """A simple container to hold discounts.
    """
    implements(IDiscountsContainer)

registerType(DiscountsContainer, PROJECTNAME)