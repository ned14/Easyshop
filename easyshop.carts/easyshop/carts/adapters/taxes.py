# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ITaxes

class CartTaxes:
    """Adapter which provides ITaxes for cart content objects.
    """
    implements(ITaxes)
    adapts(ICart)

    def __init__(self, context):
        self.context = context

    def getTaxRate(self):
        """
        """
        # Total tax rate for carts makes no sense
        raise ValueError

    def getTaxRateForCustomer(self):
        """
        """
        # Total tax rate for carts makes no sense
        raise ValueError

    def getTax(self):
        """
        """
        cart_items = self.context.objectValues()

        tax = 0.0
        for cart_item in cart_items:
            taxes = ITaxes(cart_item)
            tax += taxes.getTax()

        return tax

    def getTaxForCustomer(self):
        """
        """
        cart_items = self.context.objectValues()

        tax = 0.0
        for cart_item in cart_items:
            taxes = ITaxes(cart_item)
            tax += taxes.getTaxForCustomer()

        return tax
        
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
        price = IPrices(self.context).getPriceGross(with_discount=True)
        tax_rate = self.taxes.getTaxRate()
        
        tax  = (tax_rate/(tax_rate+100)) * price
        return tax
        
    def getTaxForCustomer(self):
        """Returns absolute tax for customer.
        """
        price = IPrices(self.context).getPriceGross(with_discount=True)
        tax_rate = self.taxes.getTaxRateForCustomer()

        tax = (tax_rate/(tax_rate+100)) * price
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