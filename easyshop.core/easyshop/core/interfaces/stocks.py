# zope imports
from zope.interface import Interface

class IStockRule(Interface):
    """A rule to calculate availability and time period of shipping.
    """

class IStockRulesContainer(Interface):
    """A simple container to holds stock rules.
    """

class IStockManagement(Interface):
    """Provides methods to manage/calculate stock rules.
    """
    def getStockRules():
        """Returns existing stock rules.
        """
        
    def getValidStockRuleFor(product):
        """Returns first valid stock rule for given product.
        """
        
    def removeCart(cart):
        """Removes product which are within given cart from stock.
        """