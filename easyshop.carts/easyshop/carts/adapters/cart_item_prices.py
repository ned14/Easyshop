# Python imports
import re

# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICartItem
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IPropertyManagement

class CartItemPrices:
    """Adapter which provides IPrices for cart item content objects.
    """
    implements(IPrices)
    adapts(ICartItem)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getPriceForCustomer(self):
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

        return price
        
    def getPriceGross(self):
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

        return price
        
    def getPriceNet(self):
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

        return price