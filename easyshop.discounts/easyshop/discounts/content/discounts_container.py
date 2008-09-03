# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IDiscountsContainer

class DiscountsContainer(OrderedBaseFolder):
    """A simple container to hold discounts.
    """
    implements(IDiscountsContainer)

registerType(DiscountsContainer, PROJECTNAME)