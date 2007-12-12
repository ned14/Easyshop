# zope imports
from zope.interface import Interface

class IPrices(Interface):
    """Provides methods to get prices.
    """
    
    def getPriceForCustomer():
       """
       """
       
    def getPriceGross():
       """
       """

    def getPriceNet():
       """
       """