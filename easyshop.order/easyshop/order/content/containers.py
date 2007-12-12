# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IOrdersContainer

class OrdersContainer(BaseBTreeFolder):
    """A simple container to hold orders.
    """
    implements(IOrdersContainer)
                 
registerType(OrdersContainer, PROJECTNAME)