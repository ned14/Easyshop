# zope imports
from zope.interface import Interface

class INumberConverter(Interface):
    """
    """
    def floatToString(float):
        """Formats a float to "0,00"
        """
        
    def formatString(string):
        """Formats a float like string to "0,00"
        """
        
    def stringToFloat(string):
        """Converts a string to a float
        """

class IAddressConverter(Interface):
    """
    """
    def addressToDict(address):
        """Returns info of given address as dict.
        """
        # Used in serveral Views.
        
class IProductConverter(Interface):
    """
    """
    def productToDict(product):
        """Returns info of given product as dict.         
        """
        # Used in serveral Views.
