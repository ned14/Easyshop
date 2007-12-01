# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import ITaxManagement
from easyshop.core.interfaces import IValidity

class ProductTaxCalculator:
    """Provides ITaxes for product content objects.
    """
    implements(ITaxes)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context
        self.shop = IShopManagement(context).getShop()

    def getTaxRate(self):
        """
        """
        return self._calcTaxRateForProduct()

    def getTaxRateForCustomer(self):
        """
        """
        return self._calcTaxRateForCustomer()        

    def getTax(self):
        """
        """
        tax_rate = self._calcTaxRateForProduct()
        price = self.context.getPrice()
        
        if self.shop.getGrossPrices() == True:
            tax_abs = (tax_rate/(tax_rate+100)) * price
        else:
            tax_abs = price * (tax_rate/100)

        return tax_abs
        
    def getTaxForCustomer(self):
        """
        """
        tax_product = self.getTax()
        tax_rate_customer = self._calcTaxRateForCustomer()
        
        if self.shop.getGrossPrices() == True:
            price_net = self.context.getPrice() - tax_product
        else:
            price_net = self.context.getPrice()
        
        return  (tax_rate_customer/100) * price_net

    def _calcTaxRateForProduct(self):
        """Calculates the default tax for a given product.
        """
        # Returns the first tax rate, which is true. Taxes are sorted by 
        # position which is also the priority
        tm = ITaxManagement(self.shop)
        for tax in tm.getDefaultTaxes():
            if IValidity(tax).isValid(self.context) == True:
                return tax.getRate()

        return 0

    def _calcTaxRateForCustomer(self):
        """Calculates the special tax for a given product and customer.
        """

        # 1. Try to find a Tax for actual Customer
        tm = ITaxManagement(self.shop)
        for tax in tm.getCustomerTaxes():
            if IValidity(tax).isValid(self.context) == True:
                return tax.getRate()

        # 2. If nothing is found, returns the default tax for the product.
        return self._calcTaxRateForProduct()