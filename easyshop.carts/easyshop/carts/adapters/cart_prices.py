# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IShopManagement

class CartPrices:
    """Adapter which provides IPrices for cart content objects.
    """
    implements(IPrices)
    adapts(ICart)
    
    def __init__(self, context):
        """
        """
        self.context = context

    # Note: Need to select whether the price is calculated with or without 
    # shipping. Otherwise it comes to recursion error if one tries to 
    # calculate the cart price in order to calculate the shipping price. See 
    # for adapters/criteria/price/isValid.
    
    # This brings the further advantage to have the flexibility whether the
    # cart price should be displayed with or without shipping price
    
    def getPriceForCustomer(self, with_shipping=True):
        """Returns the customer price of the cart. This is just a sum over 
        customer prices of all items of the cart.
        """
        price = 0.0
        for cart_item in self.context.objectValues("CartItem"):
            price += IPrices(cart_item).getPriceForCustomer()
        
        if with_shipping == True:
            sm = IShippingManagement(IShopManagement(self.context).getShop())
            shipping_price = sm.getPriceForCustomer()
            price += shipping_price

        return price

    def getPriceGross(self, with_shipping=True):
        """Returns the gross price of the cart. This is just a sum over gross
        prices of all items of the cart.
        """
        price = 0.0
        for cart_item in self.context.objectValues("CartItem"):
            price += IPrices(cart_item).getPriceGross()

        if with_shipping == True:
            sm = IShippingManagement(IShopManagement(self.context).getShop())
            shipping_price = sm.getPriceGross()
            price += shipping_price        
    
        return price

    def getPriceNet(self, with_shipping=True):
        """Returns the net price of the cart. This is just a sum over net
        prices of all items of the cart plus.
        """
        price = 0.0
        for cart_item in self.context.objectValues("CartItem"):
            price += IPrices(cart_item).getPriceNet()

        if with_shipping == True:
            sm = IShippingManagement(
                IShopManagement(self.context).getShop())
            shipping_price = sm.getPriceNet()
            price += shipping_price        

        return price

