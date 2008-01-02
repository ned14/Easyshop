    # zope imports
from zope.interface import implements
from zope.interface import Interface

# Five imports
from Products.Five.browser import BrowserView

# plone imports
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement

class ICartPortletView(Interface):
    """
    """
    def getAmountOfArticles():
        """
        """
                        
    def getCartPrice():
        """
        """
                        
    def getShopUrl():
        """
        """
        
    def showCheckOutLink():
        """
        """

class CartPortletView(BrowserView):
    """
    """
    implements(ICartPortletView)
    
    def getAmountOfArticles(self):
        """
        """
        cart = self._getCart()
        if cart is None:
            return 0
            
        amount = 0
        for item in IItemManagement(cart).getItems():
            amount += item.getAmount()
        
        return amount
                        
    def getCartPrice(self):
        """
        """
        shop = self._getShop()
        cm = ICurrencyManagement(shop)
        
        if ICartManagement(shop).hasCart():
            cart = self._getCart()
            price = IPrices(cart).getPriceForCustomer()
            return cm.priceToString(price)
        else:
            return cm.priceToString(0.0)
                        
    def getShopUrl(self):
        """
        """
        shop = self._getShop()
        return shop.absolute_url()
        
    def showCheckOutLink(self):
        """
        """
        cart = self._getCart()
        
        if cart is None:
            return False
            
        if IItemManagement(cart).hasItems() == False:
            return False
        
        return True
    
    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()

    @memoize
    def _getCart(self):
        """
        """
        shop = self._getShop()
        return ICartManagement(shop).getCart()