# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import ICart

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