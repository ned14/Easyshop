# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IFormatable
from easyshop.core.interfaces import ISearchResultContainer

class SearchResultContainer(ATFolder):
    """
    """
    implements(ISearchResultContainer, IFormatable)
                 
registerType(SearchResultContainer, PROJECTNAME)