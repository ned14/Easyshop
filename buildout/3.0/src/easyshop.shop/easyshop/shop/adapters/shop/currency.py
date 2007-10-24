# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.interface import Interface

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

class CurrencyManagement:
    """Provices currency related methods.
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
        
    def priceToString(self, price, symbol="symbol", position="before"):
        """
        """
        price = "%.2f" % price
        string = price.replace(".", ",")
        
        if symbol == "short":
            currency = self.getShortName()    
        elif symbol == "long":
            currency = self.getLongName()    
        else:
            currency = self.getSymbol()

        if position == "before":
            string = "%s %s" % (currency, string)
        else:
            string = "%s %s" % (string, currency)            

        return string        