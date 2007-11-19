# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class ProductPriceCalculator:
    """Provides IPrices for product content object
    """
    implements(IPrices)
    adapts(IProduct)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.gross_prices = IShopManagement(context).getShop().getGrossPrices()
        self.taxes = ITaxes(self.context)
        
    def getPriceForCustomer(self):
        """Returns the end price of the customer. It is the net price plus
        the tax for the customer. By default (or in most cases) this should 
        be the same price as price gross (as an customer will get the standard
        taxes of the country the shop is running).
        """        
        tax_abs_customer = self.taxes.getTaxForCustomer()
        return self.getPriceNet() + tax_abs_customer

    def getPriceNet(self):
        """Returns the net price of the product. It is just the difference of 
        price gross and the default tax (which mean the standard tax for the country
        in which the shop is running) for the product. 
        """
        if self.gross_prices == True:
            return self.context.getPriceGross() - self.taxes.getTax()
        else:
            return self.context.getPriceGross()

    def getPriceGross(self):
        """Returns the gross price of the product. This is entered by the 
        customer and the base for all other prices (price net, price for 
        customer but also for cart, cart item, order and order item)
        """
        if self.gross_prices == True:
            return self.context.getPriceGross()
        else:
            return self.context.getPriceGross() + self.taxes.getTax()
