# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import BadRequest

# easyshop imports
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentInformation
from easyshop.core.interfaces import IValidity

class PaymentInformationManagement:
    """
    """
    implements(IPaymentInformationManagement)
    adapts(ICustomer)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def deletePaymentInformation(self, id):
        """
        """
        try:    
            self.context.manage_delObjects(id)
        except BadRequest:
            return False
        else:
            return True

    def getPaymentInformation(self, id):
        """
        """
        try:
            return self.context[id]
        except KeyError:
            return None
                    
    def getPaymentInformations(self, interface=IPaymentInformation, check_validity=False):
        """Returns the payment information of a customer.
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for object in self.context.objectValues():

            if interface.providedBy(object) == False:
                continue
                
            if check_validity == True and \
               IValidity(object).isValid(object) == False:
                continue                    

            if mtool.checkPermission("View", object) is not None:
                result.append(object)
                
        return result        

    def getSelectedPaymentInformation(self, check_validity=False):
        """
        """
        try:
            selected_payment_information = \
                self.context[self.context.selected_payment_information]
        except KeyError:
            return None
        
        # If selected payment method is not valid return None
        if check_validity == False or \
           IValidity(selected_payment_information).isValid() == True:
            return selected_payment_information
        else:
            return None
            
    def getSelectedPaymentMethod(self, check_validity=False):
        """
        """
        try:
            selected_payment_method = \
                self.context.paymentmethods[self.context.selected_payment_method]
        except KeyError:
            # Return prepayment as fallback
            return self.context.paymentmethods["prepayment"]

        # Check vor validity    
        if check_validity == False or \
           IValidity(selected_payment_method).isValid() == True:
            return selected_payment_method
        else:
            # Return prepayment as fallback
            return self.context.paymentmethods["prepayment"]