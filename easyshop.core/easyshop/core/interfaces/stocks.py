# zope imports
from zope.interface import Interface

class IStockInformation(Interface):
    """Holds availability of products and time period of shipping.
    """

class IStockInformationContainer(Interface):
    """A simple container to holds stock information.
    """

class IStockManagement(Interface):
    """Provides methods to manage stock information.
    """
    def getStockInformations():
        """Returns existing stock information.
        """
        
    def getStockInformationFor(product):
        """Returns first valid stock information for given product.
        """
        
    def removeCart(cart):
        """Removes product which are within given cart from stock.
        """
        
class IAvailablility(Interface):
    """Provides calculation of availability of a product.
    """
    
    def isAvailable():
        """Returns True if the product is available.
        """