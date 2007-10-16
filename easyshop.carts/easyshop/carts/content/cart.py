# zope imports 
from zope.app.container.ordered import OrderedContainer
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from easyshop.carts.interfaces import ICart

class EasyShopCart(OrderedContainer):
    """A cart holds cart items.
    """
    implements(ICart)