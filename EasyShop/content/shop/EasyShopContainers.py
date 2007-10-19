# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IGroupsContainer
from Products.EasyShop.interfaces import IOrdersContainer

class EasyShopGroups(OrderedBaseFolder):
    """A simple container to hold groups.
    """    
    implements(IGroupsContainer)

class Orders(BaseBTreeFolder):
    """A simple container to hold orders.
    """
    implements(IOrdersContainer)
                 
registerType(EasyShopGroups, PROJECTNAME)
registerType(Orders, PROJECTNAME)