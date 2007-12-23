# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscount
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class DiscountPrices:
    """Multia adapter which provides IPrices for discount content objects and 
    product.
    """
    implements(IPrices)
    adapts(IDiscount, ICartItem)
    
    # NOTE: We need the product additionally as we need to calculate taxes, as 
    # the discount has the same tax rate as the related product.
    
    def __init__(self, discount, cart_item):
        """
        """
        self.discount  = discount
        self.cart_item = cart_item
        self.product   = cart_item.getProduct()
        self.taxes     = ITaxes(self.product)
        self.shop      = IShopManagement(self.product).getShop()

    def getPriceForCustomer(self):
        """
        """
        tax_rate_for_customer = self.taxes.getTaxRateForCustomer()
        price_net = self.getPriceNet()
    
        return price_net * ((tax_rate_for_customer+100)/100)

    def getPriceGross(self):
        """
        """
        tax_rate = self.taxes.getTaxRate()
        price = self._calcTotalPrice()
        
        if self.shop.getGrossPrices() == True:
            return price
        else:            
            return price + (price * (tax_rate/100))

    def getPriceNet(self):
        """
        """
        tax_rate = self.taxes.getTaxRate()        
        price = self._calcTotalPrice()
        
        if self.shop.getGrossPrices() == True:
            return price - (tax_rate/(tax_rate+100)) * price
        else:
            return price
            
    def _calcTotalPrice(self):
        """
        """
        if self.discount.getType() == "absolute":
            if self.discount.getBase() == "product":
                return self.cart_item.getAmount() * self.discount.getValue()

        return 0.0