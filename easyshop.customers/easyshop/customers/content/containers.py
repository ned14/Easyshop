# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import ICustomersContainer

class CustomersContainer(BaseBTreeFolder):
    """A simple container to hold customers.
    """
    implements(ICustomersContainer)        

registerType(CustomersContainer, PROJECTNAME)