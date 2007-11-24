# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IOrder
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentProcessing

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