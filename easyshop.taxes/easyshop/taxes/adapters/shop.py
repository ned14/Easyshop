# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IShop
from Products.EasyShop.interfaces import ITaxes
from Products.EasyShop.interfaces import ITaxManagement
from Products.EasyShop.interfaces import IValidity

class TaxManagement:
    """An adapter, which provides methods to manage tax objects for shop 
    context objects
    """
    implements(ITaxManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def getCustomerTaxes(self):
        """
        """
        return self.context.taxes.objectValues("CustomerTax")
        
        # Todo: Optimize        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.taxes.getPhysicalPath()),
            portal_type="CustomerTax",
            sort_on = "getObjPositionInParent",
        )

        # Todo
        return [brain.getObject() for brain in brains]

    def getDefaultTaxes(self):
        """
        """
        return self.context.taxes.objectValues("DefaultTax")
        shop = self.context.getShop()
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.taxes.getPhysicalPath()),
            portal_type="DefaultTax",
            sort_on = "getObjPositionInParent",
        )

        # Todo
        return [brain.getObject() for brain in brains]
                    
    def getTax(self, id):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = ("DefaultTax", "CustomerTax"),
            path = "/".join(self.context.taxes.getPhysicalPath()),
            id = id,
        )

        try:
            return brains[0].getObject()
        except IndexError:
            return None    
        
class Taxes:
    """An adapter, which provides taxes for shop content objects.
    """
    implements(ITaxes)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getTaxRate(self, product):
        """Returns tax rate for given product
        """
        tax = self._calcTaxForProduct(product)
        return tax

    def getTaxRateForCustomer(self, product):
        """Returns the tax rate for a given product and the actual customer
        """
        tax = self._calcTaxForCustomer(product)
        return tax

    def getTax(self, product):
        """Returns the tax absolute for given product
        """
        tax = self._calcTaxForProduct(product)
        price = product.getPriceGross()
        tax_abs = (tax/(tax+100)) * price
        return tax_abs

    def getTaxForCustomer(self, product):
        """Returns the absolute tax for a given product and the actual
        customer.
        """
        tax_product  = self.getTax(product)
        price_net    = product.getPriceGross() - tax_product
        tax_rate_customer = self._calcTaxForCustomer(product)
            
        tax_abs_customer = (tax_rate_customer/100) * price_net
        return tax_abs_customer

    def _calcTaxForProduct(self, product):
        """Calculates the tax for a given product
        """
        # return the first tax rate, which is true
        # taxes are sorted by position which is also the priority        
        tm = ITaxManagement(self.context)
        for tax in tm.getDefaultTaxes():
            if IValidity(tax).isValid(product) == True:
                return tax.getRate()

        return 0

    def _calcTaxForCustomer(self, product):
        """Calculates the tax for a given product and customer
        """

        # 1. Try to find a Tax for actual Customer
        # return the first tax rate, which is true.
        # taxes are sorted by position which is also the priority

        tm = ITaxManagement(self.context)
        for tax in tm.getCustomerTaxes():
            if IValidity(tax).isValid(product) == True:
                return tax.getRate()

        # 2. If nothing is found return the default tax for the product
        return self._calcTaxForProduct(product)