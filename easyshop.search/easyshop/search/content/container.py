# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IFormatable
from iqpp.easyshop.interfaces import ISearchResultContainer

class SearchResultContainer(ATFolder):
    """
    """
    implements(ISearchResultContainer, IFormatable)
                 
registerType(SearchResultContainer, PROJECTNAME)