# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes
from Products.Archetypes.utils import shasattr

# easyshop imports
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IOrder

class PaymentManagement:
    """Provides IPaymentManagement for order content objects.
    """
    implements(IPaymentManagement)
    adapts(IOrder)
    
    def __init__(self, context):
        """
        """
        self.context = context                  

    def deletePaymentMethod(self, id):
        """
        """            
        raise Exception
            
    def getPaymentMethods(self, methods=None):
        """
        """
        raise Exception

    def getSelectedPaymentMethod(self):
        """
        """
        customer = self.context.getCustomer()
        pm = IPaymentManagement(customer)

        return pm.getSelectedPaymentMethod()
        
    def processSelectedPaymentMethod(self):
        """
        """                                
        payment_method = self.getSelectedPaymentMethod()
        pm = IPaymentProcessing(payment_method)
        return pm.process(self.context)
        
