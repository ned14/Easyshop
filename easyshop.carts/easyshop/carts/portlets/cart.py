# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# create message factory
_ = MessageFactory("EasyShop")

# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# plone imports
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement


class ICartPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(ICartPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"Cart")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('cart.pt')

    @property
    def available(self):
        """
        """
        return True

    def update(self):
        """
        """
        self.cart_price = self.getCartPrice()
        self.shop_url = self.getShopUrl()
        self.checkout_link = self.showCheckOutLink()
        self.amount_of_articles = self.getAmountOfArticles()

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
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()
