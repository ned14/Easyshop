# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import ISessionsContainer
from iqpp.easyshop.interfaces import ICustomersContainer

class CustomersContainer(BaseBTreeFolder):
    """A simple container to hold customers.
    """
    implements(ICustomersContainer)        

class SessionsContainer(BaseBTreeFolder):
    """A simple container to hold session data.
    """
    implements(ISessionsContainer)
        
registerType(CustomersContainer, PROJECTNAME)
registerType(SessionsContainer, PROJECTNAME)