# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IGroupsContainer

class GroupsContainer(OrderedBaseFolder):
    """A simple container to hold groups.
    """    
    implements(IGroupsContainer)

registerType(GroupsContainer, PROJECTNAME)