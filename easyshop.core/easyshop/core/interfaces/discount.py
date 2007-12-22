# zope imports
from zope.interface import Interface

class IDiscount(Interface):
    """A marker interface to mark discount content objects.
    """
    
class IDiscountsContainer(Interface):
    """A marker interface for container which holds discount content objects.
    """