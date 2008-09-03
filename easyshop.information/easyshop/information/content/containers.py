# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import registerType

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IInformationContainer

class InformationContainer(ATFolder):
    """A simple container to hold information like terms and conditions.
    """
    implements(IInformationContainer)

registerType(InformationContainer, PROJECTNAME)