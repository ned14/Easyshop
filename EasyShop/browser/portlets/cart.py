# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IPrices

class IPortletShopCartView(Interface):
    """
    """
    def getCartPrice():
        """Returns current cart price.
        """
        
    def getShopUrl():
        """Returns shop url.
        """
        
    def showCheckOutLink():
        """Returns True if link to checkout is to be displayed.
        """
    
class PortletShopCartView(BrowserView):
    """
    """
    implements(IPortletShopCartView)

    def getCartPrice(self):
        """
        """        
        cart_manager = ICartManagement(self.context.getShop())
        currency_manager = ICurrencyManagement(self.context)
        
        if cart_manager.hasCart():
            cart = cart_manager.getCart()
            price = IPrices(cart).getPriceForCustomer()
            return currency_manager.priceToString(price)
        else:
            return currency_manager.priceToString(0.0)
                        
    def getShopUrl(self):
        """
        """
        shop = self.context.getShop()
        return shop.absolute_url()
        
    def showCheckOutLink(self):
        """
        """
        shop = self.context.getShop()
        cart = ICartManagement(shop).getCart()
        
        if cart is None:
            return False
            
        if IItemManagement(cart).hasItems() == False:
            return False
        
        return True