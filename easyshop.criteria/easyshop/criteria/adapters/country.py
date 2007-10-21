# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICountryCriteria
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import IShopManagement

class CountryCriteriaValidity:
    """Adapter which provides IValidity for country criteria content
    objects.
    """    
    implements(IValidity)
    adapts(ICountryCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the selected invoice address of the current customer
        has one of the selected countries.
        """
        cm = ICustomerManagement(IShopManagement(self.context).getShop())
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        invoice_address = am.getInvoiceAddress()
        
        if invoice_address and\
           invoice_address.getCountry() in self.context.getCountries():
            return True
        else:
            return False        