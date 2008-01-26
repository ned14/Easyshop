# zope imports
from zope.interface import Interface

class INumberConverter(Interface):
    """Provides several converter methods for numbers.
    """
    def floatToString(float):
        """Formats a float to "0,00"
        """

    def floatToTaxString(myfloat, unit):
        """Formats given float to a tax string like "19,0 %"
        """
        
    def formatString(string):
        """Formats a float like string to "0,00"
        """
        
    def stringToFloat(string):
        """Converts a string to a float
        """