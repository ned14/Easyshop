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
        # If the discount is by percentage, we don't have to calc the tax for 
        # the discount, because the discount is a part of the already calculated
        # price, hence we can do it here.
        
        if self.discount.getType() == "percentage":
            price = IPrices(self.cart_item).getPriceForCustomer()
            return price * (self.discount.getValue() / 100)
        else:
            tax_rate_for_customer = self.taxes.getTaxRateForCustomer()
            price_net = self.getPriceNet()
        
            # We take the net price and add the customer specific taxes.
            return price_net * ((tax_rate_for_customer+100)/100)

    def getPriceGross(self):
        """
        """
        if self.discount.getType() == "percentage":
            price = IPrices(self.cart_item).getPriceGross()
            return  price * (self.discount.getValue() / 100)
        else:
            tax_rate = self.taxes.getTaxRate()
            price = self._calcTotalPrice()

            # The price entered is considered as gross price, so we simply
            # return it.
            if self.shop.getGrossPrices() == True:
                return price                

            # The price entered is considered as net price. So we have to 
            # calculate the gross price first.
            else:
                return price * ((tax_rate+100)/100)

    def getPriceNet(self):
        """
        """
        if self.discount.getType() == "percentage":
            price = IPrices(self.cart_item).getPriceNet()
            return price * (self.discount.getValue() / 100)
        else:
            tax_rate = self.taxes.getTaxRate()
            price = self._calcTotalPrice()

            # The price entered is considered as gross price. So we have to 
            # calculate the net price first.
                
            if self.shop.getGrossPrices() == True:
                return price * (100/(tax_rate+100))
                
            # The price entered is considered as net price, so we simply return 
            # it.
            else:
                return price
            
    def _calcTotalPrice(self):
        """
        """
        if self.discount.getBase() == "cart_item":
            return self.discount.getValue()
        else:
            return self.discount.getValue() * self.cart_item.getAmount()
