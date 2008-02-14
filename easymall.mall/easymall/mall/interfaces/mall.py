# zope imports
from zope.interface import Interface

# easyshop imports
from easyshop.core.interfaces import IShop

class IMall(IShop):
    """A mall holds several shops.
    """