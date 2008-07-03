# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component import getMultiAdapter

# easyshop imports
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShippingPriceManagement
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
        self.shop = IShopManagement(context).getShop()

    # Note: Need to select whether the price is calculated with or without 
    # shipping. Otherwise it comes to recursion error if one tries to 
    # calculate the cart price in order to calculate the shipping price. See 
    # for adapters/criteria/price/isValid.
    
    # This brings the further advantage to have the flexibility whether the
    # cart price should be displayed with or without shipping price
    
    def getPriceForCustomer(self, with_shipping=True, with_payment=True, with_discount=True):
        """Returns the customer price of the cart. This is just a sum over 
        customer prices of all items of the cart.
        """
        im = IItemManagement(self.context)
        if im.hasItems() == False:
            return 0.0
        
        price = 0.0
        for cart_item in im.getItems():
            # NOTE: with_discount is passed here
            price += IPrices(cart_item).getPriceForCustomer(with_discount=with_discount)
        
        if with_shipping == True:
            sm = IShippingPriceManagement(self.shop)
            shipping_price = sm.getPriceForCustomer()
            price += shipping_price
        
        if with_payment == True:
            sm = IPaymentPriceManagement(self.shop)
            payment_price = sm.getPriceForCustomer()
            price += payment_price

        return price

    def getPriceGross(self, with_shipping=True, with_payment=True, with_discount=True):
        """Returns the gross price of the cart. This is just a sum over gross
        prices of all items of the cart plus shipping and payment.
        """
        im = IItemManagement(self.context)
        if im.hasItems() == False:
            return 0.0
        
        price = 0.0
        for cart_item in im.getItems():
            # NOTE: with_discount is passed here
            price += IPrices(cart_item).getPriceGross(with_discount=with_discount)

        if with_shipping == True:
            sm = IShippingPriceManagement(self.shop)
            shipping_price = sm.getPriceGross()
            price += shipping_price

        if with_payment == True:
            sm = IPaymentPriceManagement(self.shop)
            payment_price = sm.getPriceGross()
            price += payment_price
    
        return price

    def getPriceNet(self, with_shipping=True, with_payment=True, with_discount=True):
        """Returns the net price of the cart. This is just a sum over net
        prices of all items of the cart plus shipping and payment.
        """
        im = IItemManagement(self.context)
        if im.hasItems() == False:
            return 0.0
        
        price = 0.0
        for cart_item in im.getItems():
            # NOTE: with_discount is passed here
            price += IPrices(cart_item).getPriceNet(with_discount=with_discount)

        if with_shipping == True:
            sm = IShippingPriceManagement(self.shop)
            shipping_price = sm.getPriceNet()
            price += shipping_price        

        if with_payment == True:
            sm = IPaymentPriceManagement(self.shop)
            payment_price = sm.getPriceNet()
            price += payment_price

        return price

class CartItemPrices:
    """Adapter which provides IPrices for cart item content objects.
    """
    implements(IPrices)
    adapts(ICartItem)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getPriceForCustomer(self, with_discount=False):
        """Returns the customer price for a cart item. This is just the 
        customer product price plus the customer properties prices (can be
        positiv or negative) multiply with the amount.
        """
        product = self.context.getProduct()
        price  = IPrices(product).getPriceForCustomer()        

        # Add prices of selected properties
        pm = IPropertyManagement(product)
        for selected_property in self.context.getProperties():
            price += pm.getPriceForCustomer(
                selected_property["id"], 
                selected_property["selected_option"]
            )
        
        price *= self.context.getAmount()

        if with_discount == True:
            discount = IDiscountsCalculation(self.context).getDiscount()
            if discount is not None:
                discount_value = getMultiAdapter(
                    (discount, self.context)).getPriceForCustomer()
                price -= discount_value

        return price
        
    def getPriceGross(self, with_discount=False):
        """Returns the gross price for a cart item. This is just the gross
        product price plus the properties gross prices (can be positiv or 
        negative) multiply with the amount.
        """
        product = self.context.getProduct()
        price  = IPrices(product).getPriceGross()

        pm = IPropertyManagement(product)
        for selected_property in self.context.getProperties():
            price += pm.getPriceGross(
                selected_property["id"], 
                selected_property["selected_option"]
            )
        
        price *= self.context.getAmount()

        if with_discount == True:
            discount = IDiscountsCalculation(self.context).getDiscount()
            if discount is not None:
                discount_value = getMultiAdapter(
                    (discount, self.context)).getPriceGross()
                price -= discount_value

        return price
        
    def getPriceNet(self, with_discount=False):
        """Returns the net price for a cart item. This is just the net
        product price plus the properties net prices (can be positiv or 
        negative) multiply with the amount.
        """
        product = self.context.getProduct()
        price  = IPrices(product).getPriceNet()
        
        pm = IPropertyManagement(product)
        for selected_property in self.context.getProperties():
            price += pm.getPriceNet(
                selected_property["id"], 
                selected_property["selected_option"]
            )
        
        price *= self.context.getAmount()

        if with_discount == True:
            discount = IDiscountsCalculation(self.context).getDiscount()
            if discount is not None:
                discount_value = getMultiAdapter(
                    (discount, self.context)).getPriceNet()
                    
                price -= discount_value

        return price