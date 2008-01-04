# Zope imports
from zope import schema
from zope.app.form.interfaces import WidgetInputError
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import Interface

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IAsynchronPaymentMethod
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IStockManagement

from easyshop.core.interfaces import ITaxes
from easyshop.payment.config import ERROR, PAYED

class IOrderPreviewForm(Interface):
    """
    """
    confirmation = schema.Bool()

class OrderPreviewForm(formbase.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("order_preview.pt")
    form_fields = form.Fields(IOrderPreviewForm)
    
    def validator(self, action, data):
        """
        """
        errors = []
        if self.request.get("form.confirmation", "") == "":
            error_msg = _(u"Please confirm our terms and conditions.")
            widget = self.widgets["confirmation"]
            error = WidgetInputError(widget.name, widget.label, error_msg)
            widget._error = error
            widget.error  = error_msg
            errors.append(error)
        
        return errors
            
    @form.action(_(u"label_buy", default=u"Buy"), validator=validator, name=u'buy')
    def handle_buy_action(self, action, data):
        """Buys a cart.
        """
        putils = getToolByName(self.context, "plone_utils")
                
        # add order
        om = IOrderManagement(self.context)
        new_order = om.addOrder()

        # process payment
        result = IPaymentProcessing(new_order).process()

        # Need error for payment methods for which the customer has to pay at 
        # any case The order process should not go on if the customer is not 
        # able to pay.
        if result.code == ERROR:
            om.deleteOrder(new_order.id)
            putils.addPortalMessage(result.message, type=u"error")
            ICheckoutManagement(self.context).redirectToNextURL("ERROR_PAYMENT")
            return ""
        else:
            cm = ICartManagement(self.context)

            # Decrease stock
            IStockManagement(self.context).removeCart(cm.getCart())
            
            # Delete cart
            cm.deleteCart()

            # Set order to pending (Mails will be sent)
            wftool = getToolByName(self.context, "portal_workflow")
            wftool.doActionFor(new_order, "submit")

            putils.addPortalMessage(_(MESSAGES["ORDER_RECEIVED"]))
                        
        if result.code == PAYED:
            # Set order to payed (Mails will be sent)
            wftool = getToolByName(self.context, "portal_workflow")
            wftool.doActionFor(new_order, "pay_not_sent")

        # Redirect
        customer = \
            ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_payment_method = \
            IPaymentInformationManagement(customer).getSelectedPaymentMethod()
        
        if not IAsynchronPaymentMethod.providedBy(selected_payment_method):
            ICheckoutManagement(self.context).redirectToNextURL("BUYED_ORDER")

    def getCartItems(self):
        """Returns the items of the current cart.
        """
        cart = self._getCart()

        cm = ICurrencyManagement(self.context)
        im = IItemManagement(cart)
                
        result = []
        for cart_item in im.getItems():
            product = cart_item.getProduct()
            
            product_price = IPrices(cart_item).getPriceForCustomer() / cart_item.getAmount()
            product_price = cm.priceToString(product_price)
            
            price = IPrices(cart_item).getPriceForCustomer()

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

            # Discount
            total_price = 0
            discount = IDiscountsCalculation(cart_item).getDiscount()
            if discount is not None:
                discount_price = getMultiAdapter((discount, cart_item)).getPriceForCustomer()

                discount = {
                    "title" : discount.Title(),
                    "value" : cm.priceToString(discount_price, prefix="-"),
                }

                total_price = price - discount_price
                
            
            result.append({
                "product_title" : product.Title(),
                "product_price" : product_price,
                "properties"    : properties,
                "price"         : cm.priceToString(price),
                "amount"        : cart_item.getAmount(),
                "total_price"   : cm.priceToString(total_price),
                "discount"      : discount,
            })
        
        return result

    def getDiscounts(self):
        """
        """
        return []
        
        cart = self._getCart()        

        if cart is None: 
            return []

        cm = ICurrencyManagement(self.context)
        discounts = []
        
        for cart_item in IItemManagement(cart).getItems():
            discount = IDiscountsCalculation(cart_item).getDiscount()

            if discount is not None:
                value = getMultiAdapter((discount, cart_item)).getPriceForCustomer()
                discounts.append({
                    "title" : discount.Title(),
                    "value" : cm.priceToString(value, prefix="-"),
                })
        
        return discounts
        
    def getInvoiceAddress(self):
        """Returns invoice address of the current customer.
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return addressToDict(address)

    def getSelectedPaymentInformation(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pm = IPaymentInformationManagement(customer)
        return pm.getSelectedPaymentInformation()
        
    def getPaymentMethodInfo(self):
        """
        """
        # method
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_payment_method = customer.selected_payment_method

        pm = IPaymentMethodManagement(self.context)
        method = pm.getPaymentMethod(selected_payment_method)
        
        # price
        pp = IPaymentPriceManagement(self.context)
        payment_price = pp.getPriceGross()
        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(payment_price)
        
        return {
            "type"    : method.portal_type,
            "title"   : method.Title(),
            "price"   : price,
            "display" : payment_price != 0,
        }

    def getShippingAddress(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        address = am.getShippingAddress()

        return addressToDict(address)

    def getShippingInfo(self):
        """
        """
        sm = IShippingPriceManagement(self.context)
        shipping_price = sm.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(shipping_price)
        method = IShippingMethodManagement(self.context).getSelectedShippingMethod()
                
        return {
            "price"       : price,
            "title"       : method.Title(),
            "description" : method.Description()
        }
                
    def getTotalPrice(self):
        """
        """
        cart = self._getCart()

        pm = IPrices(cart)
        total = pm.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total)
        
    def getTotalTax(self):
        """
        """
        cart = self._getCart()
        total = ITaxes(cart).getTaxForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total)

    def hasCartItems(self):
        """
        """
        cart = self._getCart()
        
        if cart is None:
            return False
            
        im = IItemManagement(cart)
        
        if im.hasItems():
            return True
        return False

    def isCustomerComplete(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        return ICompleteness(customer).isComplete()

    def test(self, error, result_true, result_false):
        """
        """
        if error == True:
            return result_true
        else:
            return result_false

    @memoize        
    def _getCart(self):
        """Returns current cart.
        """
        return ICartManagement(self.context).getCart()
                
def addressToDict(address):
    """
    """
    return {
        "name"        : address.getName(),
        "address1"    : address.address_1,
        "zipcode"     : address.zip_code,
        "city"        : address.city,
        "country"     : address.country,
        "url"         : address.absolute_url(),
        "is_complete" : ICompleteness(address).isComplete(),
    }