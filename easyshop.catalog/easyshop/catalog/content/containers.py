# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from Products.EasyShop.config import PROJECTNAME
from Products.EasyShop.interfaces import ICategoriesContainer
from Products.EasyShop.interfaces import IProductsContainer

class ProductsContainer(BaseBTreeFolder):
    """A simple container to hold products.
    """
    implements(IProductsContainer)

class CategoriesContainer(OrderedBaseFolder):
    """A simple container to hold categories.
    """
    implements(ICategoriesContainer)

registerType(CategoriesContainer, PROJECTNAME)
registerType(ProductsContainer, PROJECTNAME)