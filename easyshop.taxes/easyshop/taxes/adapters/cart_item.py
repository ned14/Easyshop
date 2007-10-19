# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ITaxes
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import ICartItem

class CartItemTaxes:
    """Adapter which provides ITaxes for cart item content objects.
    """
    implements(ITaxes)
    adapts(ICartItem)
    
    def __init__(self, context):
        """
        """
        self.context = context

        # adapt Product to Taxes
        self.taxes = ITaxes(self.context.getProduct())

    def getTax(self):
        """Returns absolute tax.
        """
        price    = IPrices(self.context).getPriceGross()
        tax_rate = self.taxes.getTaxRate()
        
        tax  = (tax_rate/(tax_rate+100)) * price        
        return tax
        
    def getTaxForCustomer(self):
        """Returns absolute tax for customer.
        """
        price    = IPrices(self.context).getPriceGross()
        tax_rate = self.taxes.getTaxRateForCustomer()

        tax  = (tax_rate/(tax_rate+100)) * price
        return tax

    def getTaxRate(self):
        """Returns tax rate
        """
        tax_rate = self.taxes.getTaxRate()
        return tax_rate

    def getTaxRateForCustomer(self):
        """Returns tax rate for a customer.
        """
        tax = self.taxes.getTaxRateForCustomer() * self.context.getAmount()
        return tax

