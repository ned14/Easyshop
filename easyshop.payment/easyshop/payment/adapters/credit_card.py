# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IPrices

from easyshop.core.interfaces import IType

# zc.authorizedotnet import 
from zc.authorizedotnet.processing import CcProcessor

class CreditCardType:
    """Provides IType for direct debit content objects.
    """
    implements(IType)
    adapts(ICreditCard)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type of CreditCard.
        """
        return "credit-card"
        

class AuthorizeNetCreditCardPaymentProcessor:
    """Provides IPaymentProcessing for credit cards content objects.
    """
    implements(IPaymentProcessing)
    adapts(ICreditCard)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def process(self, order=None):
        """
        """
        credit_card = IPaymentManagement(order).getSelectedPaymentMethod()
        card_num = credit_card.card_number
        exp_date = credit_card.card_expiration_date

        line_items = []
        for i, item in enumerate(IItemManagement(order).getItems()):
            if item.getProductTax() > 0:
                tax = "Y"
            else:
                tax = "N"
            
            line_items.append((
                i+1,
                item.getProduct().Title(),
                item.getProductQuantity(),
                item.getProductPriceGross(),
                tax,                
            ))
            
        amount = IPrices(order).getPriceForCustomer()

        return "PAYED"
        
        cc = CcProcessor(server=SERVER_NAME, login=LOGIN, key=KEY)

        result = cc.authorize(
            amount     = amount,
            card_num   = card_num,
            exp_date   = exp_date,
            line_items = line_items)
        
        if result == "approved":
            result = cc.captureAuthorized(trans_id=result.trans_id)
        
        if result.response == "approved":
            return "PAYED"
        else:
            return "NOT_PAYED"
        
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
        """Returns true if the direct debit informations are complete.
        """        
        return True