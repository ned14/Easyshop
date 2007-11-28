# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import ICreditCardPaymentMethod
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IType
from easyshop.payment.config import PAYED, ERROR
from easyshop.payment.content import PaymentResult

# zc.authorizedotnet import 
from zc.authorizedotnet.processing import CcProcessor

class CreditCardType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of credit card payment method.
        """
        return "credit-card"
        

class AuthorizeNetCreditCardPaymentProcessor:
    """Provides IPaymentProcessing for credit cards content objects.
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

        cc = CcProcessor(
            server="test.authorize.net",
            login="39uaCH7r9K", 
            key="9ME22bvLnu87P4FY")

        result = cc.authorizeAndCapture(
            amount = amount, 
            card_num = card_num,
            exp_date = exp_date) 

        if result.response == "approved":
            return PaymentResult(PAYED, _(u"Your order has been payed."))
        else:
            return PaymentResult(ERROR, _(result.response_reason))

        # Used for captureAuthorized
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

class CreditCardPaymentMethodCompleteness:
    """
    """
    implements(ICompleteness)
    adapts(ICreditCardPaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the credit card informations are complete.
        """        
        return True
            
class CreditCardCompleteness:
    """Provides ICompleteness for direct debit content objects.
    """    
    implements(ICompleteness)
    adapts(ICreditCard)
        
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the credit card informations are complete.
        """        
        return True