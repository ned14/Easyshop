# zope imports
from zope.interface import Interface

# easyshop imports
from easyshop.core.interfaces import IProduct

class IMallProduct(IProduct):
    """A mall product has additional to the default product mall categories.
    """