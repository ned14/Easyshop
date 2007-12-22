# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class ProductPrices:
    """Provides IPrices for product content object.
    """
    implements(IPrices)
    adapts(IProduct)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.gross_prices = IShopManagement(context).getShop().getGrossPrices()
        self.taxes = ITaxes(self.context)

    def getPriceForCustomer(self, effective=True):
        """Returns the end price of the customer. It is the net price plus
        the tax for the customer. By default (or in most cases) this should 
        be the same price as price gross (as an customer will get the standard
        taxes of the country the shop is running).
        """        
        if effective == True:
            return self._getEffectivePriceForCustomer()
        else:
            return self._getStandardPriceForCustomer()
        
    def getPriceNet(self, effective=True):
        """Returns the net price of the product. It is just the difference of 
        price gross and the default tax (which mean the standard tax for the 
        country in which the shop is running) for the product. 
        """
        if effective == True:
            return self._getEffectivePriceNet()
        else:
            return self._getStandardPriceNet()

    def getPriceGross(self, effective=True):
        """Returns the gross price of the product. This is entered by the 
        customer and the base for all other prices (price net, price for 
        customer but also for cart, cart item, order and order item)
        """
        if effective == True:
            return self._getEffectivePriceGross()
        else:
            return self._getStandardPriceGross()

    # Effective Price
    def _getEffectivePriceForCustomer(self):
        """Returns the effective price for customer, dependend of whether this 
        product is for sale or not.
        """
        tax_abs_customer = self.taxes.getTaxForCustomer()
        return self._getEffectivePriceNet() + tax_abs_customer

    def _getEffectivePriceNet(self):
        """Returns the effective price net, dependend of whether this product
        is for sale or not.
        """
        if self.context.getForSale() == True:
            price = self.context.getSalePrice()
        else:
            price = self.context.getPrice()
        
        if self.gross_prices == True:
            return price - self.taxes.getTax()
        else:
            return price

    def _getEffectivePriceGross(self):
        """Returns the effective price gross, dependend of whether this product
        is for sale or not.
        """
        if self.context.getForSale() == True:
            price = self.context.getSalePrice()
        else:
            price = self.context.getPrice()
            
        if self.gross_prices == True:
            return price
        else:
            return price + self.taxes.getTax()

    # Standard Price
    def _getStandardPriceForCustomer(self):
        """Returns always the standard price, independent of whether for sale is 
        selected or not.
        """
        tax_abs_customer = self.taxes.getTaxForCustomer(False)
        return self._getStandardPriceNet() + tax_abs_customer

    def _getStandardPriceNet(self):
        """Returns always the standard price, independent of whether for sale is 
        selected or not.
        """
        if self.gross_prices == True:
            return self.context.getPrice() - self.taxes.getTax(False)
        else:
            return self.context.getPrice()

    def _getStandardPriceGross(self):
        """Returns always the standard price, independent of whether for sale is 
        selected or not.
        """
        if self.gross_prices == True:
            return self.context.getPrice()
        else:
            return self.context.getPrice() + self.taxes.getTax(False)