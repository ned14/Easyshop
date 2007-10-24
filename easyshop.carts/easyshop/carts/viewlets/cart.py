# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement

class CartViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('cart.pt')

    def update(self):
        """
        """
        self.cart_price = self.getCartPrice()
        self.shop_url = self.getShopUrl()
        self.checkout_link = self.showCheckOutLink()
        
    def getCartPrice(self):
        """
        """        
        cart_manager = ICartManagement(IShopManagement(self.context).getShop())
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
        shop = IShopManagement(self.context).getShop()
        return shop.absolute_url()
        
    def showCheckOutLink(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()
        
        if cart is None:
            return False
            
        if IItemManagement(cart).hasItems() == False:
            return False
        
        return True