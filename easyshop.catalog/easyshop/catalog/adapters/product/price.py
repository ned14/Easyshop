# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IProduct
from Products.EasyShop.interfaces import ITaxes

class ProductPriceCalculator:
    """Provides IPrices for product content object
    """
    implements(IPrices)
    adapts(IProduct)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getPriceForCustomer(self):
        """Returns the end price of the customer. It is the net price plus
        the tax for the customer. By default (or in most cases) this should 
        be the same price as price gross (as an customer will get the standard
        taxes of the country the shop is running).
        """
        tax_abs_customer = ITaxes(self.context).getTaxForCustomer()
        price = self.getPriceNet() + tax_abs_customer

        return price

    def getPriceNet(self):
        """Returns the net price of the product. It is just the difference of 
        price gross and the default tax (which mean the standard tax for the country
        in which the shop is running) for the product. 
        """
        tax_abs = ITaxes(self.context).getTax()
        price = self.context.getPriceGross() - tax_abs

        return price

    def getPriceGross(self):
        """Returns the gross price of the product. This is entered by the 
        customer and the base for all other prices (price net, price for 
        customer but also for cart, cart item, order and order item)
        """
        # just to make the adapter complete
        return self.context.getPriceGross()