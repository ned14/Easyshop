# Zope imports
from zope.interface import Interface

class ICurrencyManagement(Interface):
    """Provides methods to return different currency names.
    """
    # Todo: The whole currency stuff has to be refactored.
    def getLongName(id):
        """Returns long name for curreny with given id.
        """

    def getShortName(id):
        """Returns short name for curreny with given id.
        """
        
    def getSymbol(id):
        """Returns symbol for curreny with given id.
        """
    
    def priceToString(price, symbol="symbol", position="after"):
        """Returns given price as formated currency string.
        """