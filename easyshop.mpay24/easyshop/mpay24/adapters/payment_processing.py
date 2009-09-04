# python 
import httplib2
from urllib import quote, unquote
from datetime import datetime

# zope imports
from zope.interface import implements
from zope.component import adapts
from Products.CMFPlone.utils import log

# easyshop imports
from easyshop.mpay24.interfaces import ImPAY24PaymentMethod
from easyshop.mpay24 import EasyShopMPAY24MessageFactory as _
from easyshop.core.interfaces import IAddressManagement, \
                                     ICustomerManagement, \
                                     IItemManagement, \
                                     IPaymentInformationManagement, \
                                     IPaymentProcessing, \
                                     IPrices, \
                                     IShopManagement
from easyshop.payment.config import PAYED, NOT_PAYED, ERROR
from easyshop.payment.content import PaymentResult


class mPAY24CardPaymentProcessor:
    """Provides IPaymentProcessing for credit cards content objects using 
    Authorize.net.
    """
    implements(IPaymentProcessing)
    adapts(ImPAY24PaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        shop        = IShopManagement(self.context).getShop()
        customer    = ICustomerManagement(shop).getAuthenticatedCustomer()
        
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
        
        mpay24_url = self.context.getUrl()
        mpay24_merchant_id = self.context.getMerchant_id()
        mpay24_mdxi = self.context.getMdxi()
        
        conn_query = "OPERATION=SELECTPAYMENT&MERCHANTID=%s&MDXI=%s" % \
            (mpay24_merchant_id,
             quote(mpay24_mdxi % dict(tid=order.id,
                                      price=amount,
                                      site_url=shop.absolute_url())),)
                                
        conn_string = "%s?%s" % (mpay24_url, conn_query)
             
        h = httplib2.Http('.cache',timeout=10)
        http_response, data = h.request(conn_string,"GET",)
        
        if data:
            data_dict = dict([part.split('=') for part in data.split('&')])
            
            if data_dict.get('STATUS','')=='ERROR':
                return PaymentResult(ERROR,"%s\n%s" % \
                    (unquote(data_dict.get('RETURNCODE','')),
                     unquote(conn_string)))
            else:
                if data_dict.get('RETURNCODE','')=='REDIRECT':
                    new_loc = unquote(data_dict.get('LOCATION','').strip())
                    log("redirecting mPAY24 request to %s" % new_loc)
                    return PaymentResult('MPAY24', new_loc)
                else:
                    return PaymentResult(ERROR, data_dict)
                    
        return PaymentResult(ERROR,_("no data"))
        