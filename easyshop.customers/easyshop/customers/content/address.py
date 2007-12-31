# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IAddress

class Address(BaseContent):
    """
    """
    implements(IAddress)

    def Title(self):
        """
        """
        return self.getName()
        
    def getName(self, reverse=False):
        """
        """
        if reverse:
            name = self.lastname
            if name != "": name += ", "
            name += self.firstname
        else:
            name = self.firstname
            if name != "": name += " "
            name += self.lastname
        
        return name

registerType(Address, PROJECTNAME)