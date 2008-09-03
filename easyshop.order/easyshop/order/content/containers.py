# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IOrdersContainer

class OrdersContainer(BaseBTreeFolder):
    """A simple container to hold orders.
    """
    implements(IOrdersContainer)
                 
registerType(OrdersContainer, PROJECTNAME)