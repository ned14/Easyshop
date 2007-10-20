# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import IGroupsContainer

class GroupsContainer(OrderedBaseFolder):
    """A simple container to hold groups.
    """    
    implements(IGroupsContainer)

registerType(GroupsContainer, PROJECTNAME)