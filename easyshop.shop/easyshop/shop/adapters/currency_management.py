# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.interface import Interface

# easyshop imports
from easyshop.core.config import CURRENCIES
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IShopManagement

class CurrencyManagement:
    """Provides ICurrencyManagement for serveral content objects.
    """
    implements(ICurrencyManagement)
    adapts(Interface)
    
    def __init__(self, context):
        """
        """
        self.shop = IShopManagement(context).getShop()
        
    def getLongName(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]["long"]
        
    def getShortName(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]["short"]
        
    def getSymbol(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]["symbol"]
        
    def priceToString(self, price, symbol="symbol", position="before", prefix=None, suffix="*"):
        """
        """
        price = "%.2f" % price
        price = price.replace(".", ",")
        
        if symbol == "short":
            currency = self.getShortName()    
        elif symbol == "long":
            currency = self.getLongName()    
        else:
            currency = self.getSymbol()

        if prefix is not None:
            price = "%s%s" % (prefix, price)

        if suffix is not None:
            price = "%s%s" % (price, suffix)
            
        if position == "before":
            price = "%s %s" % (currency, price)
        else:
            price = "%s %s" % (price, currency)

        return price