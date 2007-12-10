# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentMethodCriteria
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class PaymentMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IPaymentMethodCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the selected payment method of the current customer 
        is within the selected payment methods of the criterion.
        """
        shop = IShopManagement(self.context).getShop()
        
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()        
        customer_payment_method = customer.selected_payment_method
        
        if customer_payment_method in self.context.getPaymentMethods():
            return True
        else:
            return False