# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IPaymentMethodCriteria
from Products.EasyShop.interfaces import IValidity

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
        shop = self.context.getShop()
        
        cm = ICustomerManagement(shop)
        customer = cm.getAuthenticatedCustomer()
        
        pm = IPaymentManagement(customer)
        customer_payment_method = pm.getSelectedPaymentMethod().getId()
                
        if customer_payment_method in self.context.getPaymentMethods():
            return True
        else:
            return False