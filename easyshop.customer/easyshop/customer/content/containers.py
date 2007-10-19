# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import ICustomersContainer

class Customers(BaseBTreeFolder):
    """A simple container to hold customers.
    """
    implements(ICustomersContainer)        

registerType(Customers, PROJECTNAME)