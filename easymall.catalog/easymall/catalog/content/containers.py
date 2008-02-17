# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# easyshop imports
from easyshop.core.interfaces import ICategoriesContainer
from easyshop.core.interfaces import IProductsContainer

# easymall imports
from easymall.mall.config import PROJECTNAME
from easymall.mall.interfaces import IMallCategoriesContainer

class MallCategoriesContainer(OrderedBaseFolder):
    """A simple container to hold categories.
    """
    implements(IMallCategoriesContainer)

registerType(MallCategoriesContainer, PROJECTNAME)
