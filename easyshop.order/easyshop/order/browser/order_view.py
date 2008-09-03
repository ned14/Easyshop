from AccessControl import Unauthorized

# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IType

class IOrderView(Interface):
    """View for order content objects.
    """
    def getCreationDate():
        """Returns the creation date.
        """
        
    def getCustomerFullname():
        """Returns the customer name.        
        It is taken from the invoice address of the order.
        """

    def getEmail():
        """Returns email of the order's customer.
        """
        
    def getItems():
        """Returns the items.
        """

    def getPaymentValues():
        """Returns prices and taxes for selectec payment method.
        """    
        
    def getSelectedPaymentData():
        """Returns the payment method of the current customer.
        """
        
    def getPriceForCustomer():
        """Returns the total price for the customer.
        """

    def getInvoiceAddress():
        """Returns the invoice address.
        """    
    
    def getShippingAddress():
        """Returns the shipping address.
        """    

    def getShipping():
        """Returns the shipping prices as dict.
        """

    def getState():
        """Returns the workflow state of the order.
        """

    def isPaymentAllowed():
        """Returns True if the redo of a payment is allowed.
        """
            
    def pay():
        """Does the payment process.

        This is used for payment with paypal, at the moment, when the customer
        knows that something has gone wrong (broken connection, etc.) for the 
        first time.
        """    
        
class OrderView(BrowserView):
    """
    """
    implements(IOrderView)

    def getCreationDate(self):
        """
        """
        date = self.context.created()        
        
        tool = getToolByName(self.context, 'translation_service')
        return tool.ulocalized_time(date, long_format=True)
                
    def getCustomerFullname(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return address.getName()

    def getEmail(self):
        """
        """                
        # Todo: Create an adapter Address Management for IOrder
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        return address.email
                
    def getItems(self):
        """
        """    
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        
        items = []
        item_manager = IItemManagement(self.context)
        for item in item_manager.getItems():

            product_price_gross = cm.priceToString(item.getProductPriceGross(), suffix=None)
            tax_rate = nc.floatToTaxString(item.getTaxRate())
            tax = cm.priceToString(item.getTax(), suffix=None)
            price_gross = cm.priceToString(item.getPriceGross(), suffix=None)

            # Get url. Takes care of, if the product has been deleted in the 
            # meanwhile.
            product = item.getProduct()
            if product is None:
                url = None
            else:
                url = product.absolute_url()
            
            # Properties 
            for property in item.getProperties():
                if IProductVariant.providedBy(product) == True:
                    property["show_price"] = False
                else:
                    property["show_price"] = True
                
            temp = {
                "product_title"        : item.getProductTitle(),
                "product_quantity"     : item.getProductQuantity(),
                "product_url"          : url,
                "product_price_gross"  : product_price_gross,
                "price_gross"          : price_gross,
                "tax_rate"             : tax_rate,
                "tax"                  : tax,
                "properties"           : item.getProperties(),
                "has_discount"         : abs(item.getDiscountGross()) > 0,
                "discount_description" : item.getDiscountDescription(),
                "discount"             : cm.priceToString(item.getDiscountGross(), prefix="-", suffix=None),
            }
            
            items.append(temp)

        return items

    def getPaymentValues(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getPaymentPriceNet(), suffix=None)
        price_gross = cm.priceToString(self.context.getPaymentPriceGross(), suffix=None)
        tax_rate = nc.floatToTaxString(self.context.getPaymentTaxRate())
        tax = cm.priceToString(self.context.getPaymentTax(), suffix=None)
        
        return {
            "display" : self.context.getPaymentPriceGross() != 0,
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax, 
            "title" : "Cash on Delivery"
        }

    def getSelectedPaymentData(self):
        """Returns selected payment method type and corresponding selected 
        payment information.
        """
        customer = self.context.getCustomer()
        pm = IPaymentInformationManagement(customer)
        
        payment_information     = pm.getSelectedPaymentInformation()
        selected_payment_method = pm.getSelectedPaymentMethod()

        return {
            "information"    : payment_information,
            "portal_type"    : selected_payment_method.portal_type,
            "payment_method" : selected_payment_method
        }
        
    def getPriceForCustomer(self):
        """
        """
        p = IPrices(self.context)        
        price = p.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price, suffix=None)
        
    def getInvoiceAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder 
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.company_name,
            "address1" : address.address_1,
            "zipcode" : address.zip_code,
            "city": address.city,
            "country" : address.country,
            "phone" : address.phone           
        }

    def getOverviewURL(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()
        return "%s/my-orders" % customer.absolute_url()
                
    def getShippingAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.company_name,
            "address1" : address.address_1,
            "zipcode" : address.zip_code,
            "city": address.city,
            "country" : address.country,
            "phone" : address.phone           
        }

    def getShipping(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getShippingPriceNet(), suffix=None)
        price_gross = cm.priceToString(self.context.getShippingPriceGross(), suffix=None)
        tax_rate = nc.floatToTaxString(self.context.getShippingTaxRate())
        tax = cm.priceToString(self.context.getShippingTax(), suffix=None)
        
        return {
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax,    
        }
    
    def getState(self):
        """
        """
        wftool = getToolByName(self.context, "portal_workflow")
        return wftool.getInfoFor(self.context, "review_state")

    def getTax(self):
        """
        """
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(self.context.getTax(), suffix=None)
        
    def isPaymentAllowed(self):
        """
        """
        pm = IPaymentInformationManagement(self.context.getCustomer())
        m = pm.getSelectedPaymentMethod()
        
        if IType(m).getType() not in REDO_PAYMENT_PAYMENT_METHODS:
            return False

        wftool = getToolByName(self.context, "portal_workflow")
        state = wftool.getInfoFor(self.context, "review_state")
        
        if state not in REDO_PAYMENT_STATES:
            return False

        return True

    def pay(self):
        """
        """
        # ATM only PayPal is allowed, so I haven't to differ and no redirect
        # is needed as the paypal process redirects to paypal.com
        if self.isPaymentAllowed():
            IPaymentProcessing(self.context).process()
