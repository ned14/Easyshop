# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from iqpp.easyshop.config import PROJECTNAME
from iqpp.easyshop.interfaces import IStockInformationContainer

class StockInformationContainer(OrderedBaseFolder):
    """A simple container to hold stock information.
    """
    implements(IStockInformationContainer)

registerType(StockInformationContainer, PROJECTNAME)