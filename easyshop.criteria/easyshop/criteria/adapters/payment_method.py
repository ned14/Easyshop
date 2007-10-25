# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentMethodCriteria
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class PaymentMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content
    objects.
    """
    implements(IValidity)
    adapts(IPaymentMethodCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether the selected payment method of the current customer
        is within selected payment methods.
        """
        shop = IShopManagement(self.context).getShop()
        
        cm = ICustomerManagement(shop)
        customer = cm.getAuthenticatedCustomer()
        
        pm = IPaymentManagement(customer)
        customer_payment_method = pm.getSelectedPaymentMethod().getId()
                
        if customer_payment_method in self.context.getPaymentMethods():
            return True
        else:
            return False