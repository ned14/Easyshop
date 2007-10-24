# Zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.i18nmessageid import MessageFactory

# Five imports
from Products.Five.browser import BrowserView 

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentPrices
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IType
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IShopManagement

_ = MessageFactory("EasyShop")

class IOrderPreviewView(Interface):    
    """
    """
    def buy():
        """Buys a cart
        """

    def getCart():
        """Returns current cart.
        """
        
    def getCartItems():
        """Returns the items of the current cart.
        """

    def getInvoiceAddress():
        """Returns invoice address of the current customer.
        """

    def getSelectedPaymentMethod():
        """Returns the selected payment method.
        """
        
    def getPaymentMethodInfo():
        """Returns some info of the current payment method of the current
        customer
        """

    def getPaymentMethodType():
        """Returns the type of the selected payment method of current customer.
        Note: This is also part of the returned info of getPaymentMethodInfo.
        """
        
    def getShippingAddress():
        """Returns shipping address of the current customer.
        """

    def getShippingMethodInfo():
        """Returns some info of the selected payment method of the current
        customer
        """

    def showShippingNote():
        """Returns True if a note to shipping price is meant to be displayed.
        """
        
    def getShippingPrice():
        """Returns the shipping price for current cart of current customer.
        """

    def getTotalPrice():
        """Returns product price (the total price of the cart) plus shipping.
        price
        """
        
    def getTotalTax():
        """Returns product tax plus shipping tax.
        """

    def hasCartItems():
        """Returns True if the current cart has items.
        """        

    def isCustomerComplete():
        """Returns True if current customer is ready to check out.
        """

    def isPaymentComplete():
        """Returns True if the information for the current payment method is
        complete entered.
        """    
        
    def showPaymentMethodEditButton():
        """Returns True if the button is meant to be displayed.
        """

    def showPayPalForm():
        """Returns True if the paypal form is meant to be displayed.
        """
        
class OrderPreviewView(BrowserView):
    """
    """
    implements(IOrderPreviewView)

    def __init__(self, context, request):
        """
        """
        super(OrderPreviewView, self).__init__(context, request)
        self.shop = self.context
                
    def buy(self):
        """
        """
        putils = getToolByName(self.shop, "plone_utils")
                
        # get customer
        customer = ICustomerManagement(self.shop).getAuthenticatedCustomer()

        # add order
        om = IOrderManagement(self.shop)
        new_order = om.addOrder()

        # process payment
        pm = IPaymentManagement(new_order)
        result = pm.processSelectedPaymentMethod()

        # Need error for payment methods, who the customer has to pay at any case
        # The order process should not go on if the customer could not pay.
        if result == "PAYMENT_ERROR":
            return
                    
        if result == "PAYED":
            wftool = getToolByName(self, "portal_workflow")
            wftool.doActionFor(new_order, "pay")

        putils.addPortalMessage(_(MESSAGES["ORDER_RECEIVED"]))

        # redirect
        if pm.getSelectedPaymentMethod().portal_type != "PayPal":
            self.context.request.response.redirect(self.context.absolute_url())

    def getCart(self):
        """Returns current cart.
        """
        cm = ICartManagement(self.shop)
        return cm.getCart()

    def getCartItems(self):
        """
        """            
        cm = ICartManagement(self.shop)
        cart = cm.getCart()

        cm = ICurrencyManagement(self.shop)
        im = IItemManagement(cart)
                
        result = []
        for cart_item in im.getItems():
            product = cart_item.getProduct()
            
            product_price = IPrices(cart_item).getPriceForCustomer() / cart_item.getAmount()
            product_price = cm.priceToString(product_price)
            
            price = IPrices(cart_item).getPriceForCustomer()
            price = cm.priceToString(price)

            # Todo: Think about to factoring out properties stuff
            # because same has to be uses there: cart.py / getCartItems()
            properties = []
            pm = IPropertyManagement(product)
            for selected_property in cart_item.getProperties():
                property_price = pm.getPriceForCustomer(
                    selected_property["id"], 
                    selected_property["selected_option"]) 

                # This could happen if a property is deleted and there are 
                # still product with this selected property in the cart.
                # Todo: Think about, whether theses properties are not to 
                # display. See also cart.py
                try:                                        
                    property_title = pm.getProperty(
                        selected_property["id"]).Title()
                except AttributeError:
                    property_title = selected_property["id"]
                
                properties.append({
                    "id" : selected_property["id"],
                    "selected_option" : selected_property["selected_option"],
                    "title" : property_title,
                    "price" : cm.priceToString(property_price)
                })
            
            result.append({
                "product_title" : product.Title(),
                "product_price" : product_price,
                "properties"    : properties,
                "price"         : price,
                "amount"        : cart_item.getAmount(),
            })
        
        return result
        
    def getInvoiceAddress(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return addressToDict(address)

    def getSelectedPaymentMethod(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()        
        pm = IPaymentManagement(customer)
        return pm.getSelectedPaymentMethod()
        
    def getPaymentMethodInfo(self):
        """
        """                
        # method
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()        
        pm = IPaymentManagement(customer)
        method = pm.getSelectedPaymentMethod()
        
        # price
        pp = IPaymentPrices(self.context)
        payment_price = pp.getPriceGross()
        cm = ICurrencyManagement(self.shop)
        price = cm.priceToString(payment_price)
        
        return {
            "type"    : IType(method).getType(),
            "title"   : method.Title(),
            "price"   : price,
            "display" : payment_price != 0,
        }

    def getPaymentMethodType(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()        
        pm = IPaymentManagement(customer)
        method = pm.getSelectedPaymentMethod()
        
        return IType(method).getType()

        
    def getShippingAddress(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        address = am.getShippingAddress()

        return addressToDict(address)

    def getShippingMethodInfo(self):
        """
        """
        pm = IShippingManagement(self.shop)
        shipping_method = pm.getSelectedShippingMethod()
        
        return {
            "title"       : shipping_method.Title(),
            "description" : shipping_method.Description(),
        }
                
    def showShippingNote(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()

        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        if address.getCountry() != "Deutschland":
            return True
        else:
            return False
        
    def getShippingPrice(self):
        """
        """        
        sm = IShippingManagement(self.shop)
        shipping_price = sm.getPriceForCustomer()

        cm = ICurrencyManagement(self.shop)
        return cm.priceToString(shipping_price)
                
    def getTotalPrice(self):
        """
        """
        cart = ICartManagement(self.shop).getCart()                

        pm = IPrices(cart)        
        total = pm.getPriceForCustomer()

        # Todo: Should this be in cart?
        pp = IPaymentPrices(self.context)
        total += pp.getPriceGross()
        
        cm = ICurrencyManagement(self.shop)
        total = cm.priceToString(total)
        
        return total
        
    def getTotalTax(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()

        t = ITaxes(cart)
        sm = IShippingManagement(shop)
        
        total = t.getTaxForCustomer() + sm.getTaxForCustomer()

        # Todo: Should this be in cart?
        pp = IPaymentPrices(self.context)
        total += pp.getTaxForCustomer()

        cm = ICurrencyManagement(self.shop)        
        total = cm.priceToString(total)
        
        return total

    def hasCartItems(self):
        """
        """
        cart = ICartManagement(self.shop).getCart()
        
        if cart is None:
            return False
            
        im = IItemManagement(cart)
        
        if im.hasItems():
            return True
        return False

    def isCustomerComplete(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()
        
        return ICompleteness(customer).isComplete()

    def isPaymentComplete(self):
        """
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()
        
        pm = IPaymentManagement(customer)
        method = pm.getSelectedPaymentMethod()

        return ICompleteness(method).isComplete()

    def showPaymentMethodEditButton(self):
        """
        """        
        # get customer
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        payment_method = IPaymentManagement(customer).getSelectedPaymentMethod()        
        type_manager = IType(payment_method) 
        
        if type_manager.getType() in ("prepayment", "paypal"):
            return False
        return True
        
    def showPayPalForm(self):
        """
        """
        # Todo: Use interface instead of type
        if self.getPaymentMethodType() == "paypal":
            return True
        return False
        
def addressToDict(address):
    """
    """
    return {
        "name"        : address.getName(),
        "address1"    : address.getAddress1(),
        "address2"    : address.getAddress2(),        
        "zipcode"     : address.getZipCode(),
        "city"        : address.getCity(),
        "country"     : address.getCountry(),
        "url"         : address.absolute_url(),
        "is_complete" : ICompleteness(address).isComplete(),
    }