# zope imports
from zope.interface import Interface

class IDiscount(Interface):
    """A marker interface to mark discount content objects.
    """
    
class IDiscountsContainer(Interface):
    """A marker interface for container which holds discount content objects.
    """
    
class IDiscountsManagement(Interface):
    """Provides management of discount content objects.
    """
    def getDiscounts():
        """Returns discount content objects.
        """

class IDiscountsCalculation(Interface):
    """Provides calculation of discounts.
    """
    def getDiscounts():
        """Returns calculated discounts as dictionary.
        """
