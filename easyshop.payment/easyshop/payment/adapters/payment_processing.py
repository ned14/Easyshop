# python 
import urllib

# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import PAYPAL_URL
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICreditCardPaymentMethod
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IDirectDebitPaymentMethod
from easyshop.core.interfaces import IGenericPaymentMethod
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrder
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPayPalPaymentMethod
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.payment.config import PAYED, NOT_PAYED, ERROR
from easyshop.payment.content import PaymentResult

from zc.authorizedotnet.processing import CcProcessor
class EasyShopCcProcessor(CcProcessor):
    """A small wrapper around zc.authorizedotnet to add an authorizeAndCapture 
    method.
    """
    def authorizeAndCapture(self, **kws):
        if not isinstance(kws['amount'], basestring):
            raise ValueError('amount must be a string')
        
        type = 'AUTH_CAPTURE'

        result = self.connection.sendTransaction(type=type, **kws)
        return result
        
class AuthorizeNetCreditCardPaymentProcessor:
    """Provides IPaymentProcessing for credit cards content objects using 
    Authorize.net.
    """
    implements(IPaymentProcessing)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        shop        = IShopManagement(self.context).getShop()
        customer    = ICustomerManagement(shop).getAuthenticatedCustomer()
        credit_card = IPaymentInformationManagement(customer).getSelectedPaymentInformation()
        
        card_num = credit_card.card_number
        exp_date = "%s/%s" % (credit_card.card_expiration_date_month,
                              credit_card.card_expiration_date_year)

        line_items = []
        for i, item in enumerate(IItemManagement(order).getItems()):
            if item.getProductTax() > 0:
                tax = "Y"
            else:
                tax = "N"
            
            line_items.append((
                str(i+1),
                item.getProduct().Title(),
                str(item.getProductQuantity()),
                str(item.getProductPriceGross()),
                tax,                
            ))
            
        amount = "%.2f" % IPrices(order).getPriceForCustomer()

        cc = EasyShopCcProcessor(
            server="test.authorize.net",
            login="39uaCH7r9K", 
            key="9ME22bvLnu87P4FY")

        # Used for authorizeAndCapture
        result = cc.authorizeAndCapture(
            amount = amount, 
            card_num = card_num,
            exp_date = exp_date) 
        if result.response == "approved":
            return PaymentResult(PAYED, _(u"Your order has been payed."))
        else:
            return PaymentResult(ERROR, _(result.response_reason))

        # # Used for captureAuthorized
        # authorize_result = cc.authorize(
        #     amount = amount, 
        #     card_num = card_num,
        #     exp_date = exp_date)
        # 
        # if authorize_result.response == "approved":
        #     capture_result = cc.captureAuthorized(
        #         trans_id=authorize_result.trans_id,
        #         approval_code = authorize_result.approval_code
        #     )
        #     
        #     if capture_result.response == "approved":
        #         return PaymentResult(PAYED, _(u"Your order has been payed."))
        #     else:
        #         return PaymentResult(ERROR, _(capture_result.response_reason))
        # else:
        #     return PaymentResult(ERROR, _(authorize_result.response_reason))

class DirectDebitPaymentProcessor:
    """Provides IPaymentProcessing for direct debit payment method.
    """
    implements(IPaymentProcessing)
    adapts(IDirectDebitPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """        
        return PaymentResult(NOT_PAYED, "")

class GenericPaymentProcessor:
    """Provides IPaymentProcessing for simple payment content objects.
    """
    implements(IPaymentProcessing)
    adapts(IGenericPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        if self.context.getPayed() == True:
            code = PAYED
        else:
            code = NOT_PAYED
            
        return PaymentResult(code, "")                        

class OrderPaymentProcessor:
    """Provides IPaymentProcessing for orders.
    """
    implements(IPaymentProcessing)
    adapts(IOrder)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self):
        """
        """
        customer = self.context.getCustomer()
        pm = IPaymentInformationManagement(customer)
        payment_method = pm.getSelectedPaymentMethod()
        
        return IPaymentProcessing(payment_method).process(self.context)
        
class PayPalPaymentProcessor:
    """Provides IPaymentProcessing for paypal content objects.
    Passes the whole cart to paypal. (There can be a problem because the
    content is passed via GET-REQUEST)
    """
    implements(IPaymentProcessing)
    adapts(IPayPalPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order):
        """
        """
        info = dict()

        pc = IPrices(order)
        
        url = "https://www.sandbox.paypal.com/cgi-bin/webscr"
        
        customer = order.getCustomer()

        am = IAddressManagement(customer)
        invoice_address  = am.getInvoiceAddress()
        shipping_address = am.getShippingAddress()
                
        info = {
            "cmd" : "_cart",
            "upload" : "1",
            "business" : "heinz@haendler.de",
            "currency_code" : "EUR",
            "notify_url" : "",
            "return" : "",
            "last_name" : shipping_address.getName(),
            "address1" : shipping_address.address_1,
            "city" : shipping_address.city,
            "state" : shipping_address.country,
            "zip" : shipping_address.zip_code,
            "shipping_1" : order.getShippingPriceNet(),
            "tax_1" : pc.getPriceGross() - pc.getPriceNet()
        }
        
        im = IItemManagement(order)
        for i, item in enumerate(im.getItems()):
            j = i + 1
            name     = "item_name_%s" % j
            quantity = "quantity_%s" % j
            amount   = "amount_%s" % j
            
            product = item.getProduct()
            
            info[name]     = product.Title()
            info[quantity] = str(int(item.getProductQuantity()))
            info[amount]   = str(item.getProductPriceGross())
            
        # redirect to paypal    
        parameters = "&".join(["%s=%s" % (k, v) for (k, v) in info.items()])                
        
        url = url + "?" + parameters
        self.context.REQUEST.RESPONSE.redirect(url)
        
        return PaymentResult(NOT_PAYED)
        
class PayPalSimplePaymentProcessor:
    """Provides IPaymentProcessing for paypal content objects. Passes just a 
    value for the whole cart to PayPal.
    """
    implements(IPaymentProcessing)
    adapts(IPayPalPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """    
        info = dict()

        shop = IShopManagement(self.context).getShop()                        
        notify_url = "%s/paypal?order=%s" % (shop.absolute_url(), order.UID())
        return_url = "%s/thank-you" % shop.absolute_url()
        
        pc = IPrices(order)
        price_net = "%.2f" % pc.getPriceNet()
        tax = "%.2f" % (pc.getPriceGross() - float(price_net))
                
        customer = order.getCustomer()
        am = IAddressManagement(customer)
        invoice_address  = am.getInvoiceAddress()
        shipping_address = am.getShippingAddress()

        site_encoding = self.context.plone_utils.getSiteEncoding()
        
        info = {
            "cmd" : "_xclick",
            "upload" : "1",
            "business" : shop.getPayPalId(),
            "currency_code" : "EUR",
            "notify_url" : notify_url,
            "return" : return_url,
            "first_name" : invoice_address.firstname.encode(site_encoding),
            "last_name" : invoice_address.lastname.encode(site_encoding),
            "address1" : invoice_address.address_1.encode(site_encoding),
            "address2" : "",
            "city" : invoice_address.city.encode(site_encoding),
            "state" : invoice_address.country.encode(site_encoding),
            "zip" : invoice_address.zip_code.encode(site_encoding),
            "no_shipping" : "1",
            "item_name" : shop.getShopOwner(),
            "amount" : price_net,
            "tax" : tax,
        }

        # redirect to paypal    
        parameters = "&".join(["%s=%s" % (k, v) for (k, v) in info.items()])
        
        url = PAYPAL_URL + "?" + parameters
        self.context.REQUEST.RESPONSE.redirect(url)
        
        return PaymentResult(NOT_PAYED)