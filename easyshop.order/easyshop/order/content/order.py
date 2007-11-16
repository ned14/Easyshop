# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.interfaces import IOrder
from easyshop.core.config import *
from easyshop.core.interfaces import IAddressManagement

schema = Schema((

    FloatField(
        name='paymentPriceNet',
        widget=DecimalWidget(
            label='Payment Price Net',
            label_msgid='schema_payment_price_net_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='paymentPriceGross',
        widget=DecimalWidget(
            label='Payment Price Gross',
            label_msgid='schema_payment_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='paymentTaxRate',
        widget=DecimalWidget(
            label='Payment Tax Rate',
            label_msgid='schema_payment_tax_rate_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='paymentTax',
        widget=DecimalWidget(
            label='Payment Tax',
            label_msgid='schema_payment_tax_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='shippingPriceNet',
        widget=DecimalWidget(
            label='Shipping Price Net',
            label_msgid='schema_shipping_price_net_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='shippingPriceGross',
        widget=DecimalWidget(
            label='Shipping Price Gross',
            label_msgid='schema_shipping_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='shippingTaxRate',
        widget=DecimalWidget(
            label='Shipping Tax Rate',
            label_msgid='schema_shipping_tax_rate_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='shippingTax',
        widget=DecimalWidget(
            label='Shipping Tax',
            label_msgid='schema_shipping_tax_label',
            i18n_domain='EasyShop',
        )
    ),
))

class Order(BaseFolder):
    """A Order holds OrderItems. 
    
       Further it holds a copy of the current customer object at the moment
       the customer has buyed his cart.
    """
    implements(IOrder)
    security = ClassSecurityInfo()    
    _at_rename_after_creation = True    

    schema = BaseSchema.copy() + schema.copy()
        
    security.declarePublic('getCustomer')
    def getCustomer(self):
        """Returns the customer of the order
        """
        catalog = getToolByName(self, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.getPhysicalPath()),
            portal_type = "Customer",
        )
        
        try:
            return brains[0].getObject()
        except IndexError:
            return None

    security.declarePublic('SearchableText')    
    def SearchableText(self):
        """
        """
        text = self.id

        # addresses
        customer = self.getCustomer()
        if customer is not None:
            for address in customer.objectValues("Address"):
                text += " "
                text += " ".join((address.firstname,
                                  address.lastname,
                                  address.address_1,
                                  address.zip_code,
                                  address.city))
        return text

    def Description(self):
        """Makes search results more informative.
        """
        customer = self.getCustomer()
        if customer is None:
            return ""

        address = IAddressManagement(customer).getInvoiceAddress()            
        if address is None:
            return ""

        description  = address.firstname + " " 
        description += address.lastname  + " - "
        description += address.address_1 + ", "
        description += address.zip_code  + " "
        description += address.city

        return description

    def fullname(self):
        """To sort orders on fullname.
        """
        customer = self.getCustomer()
        if customer is None:
            return ""        

        address = IAddressManagement(customer).getInvoiceAddress()
        if address is None:
            return ""
        
        return address.lastname + " " + address.firstname
        
registerType(Order, PROJECTNAME)