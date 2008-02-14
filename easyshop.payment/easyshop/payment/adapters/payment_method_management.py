# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IPaymentMethod
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import ISelectablePaymentMethod
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IValidity

class PaymentMethodManagement(object):
    """An adapter which provides IPaymentMethodManagement for shop content
    objects.
    """
    implements(IPaymentMethodManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.paymentmethods = self.context.paymentmethods

    def deletePaymentMethod(self, id):
        """
        """
        try:
            self.context.paymentmethods.manage_delObjects(id)
        except AttributeError:
            return False

        return True

    def getPaymentMethod(self, id):
        """Returns payment method by given id.
        """
        try:
            return self.paymentmethods[id]
        except KeyError:
            return None

    def getPaymentMethods(self, check_validity=False):
        """Returns the payment methods on shop level. 
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for object in self.paymentmethods.objectValues():

            if IPaymentMethod.providedBy(object) == False:
                continue

            if check_validity and \
               IValidity(object).isValid(object) == False:
                continue                    
            
            if mtool.checkPermission("View", object) is not None:
                result.append(object)
        
        return result
            
    def getSelectablePaymentMethods(self, check_validity=False):
        """Returns payment method which are selectable by a customer.
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for object in self.paymentmethods.objectValues():

            if ISelectablePaymentMethod.providedBy(object) == False:
                continue

            if check_validity and \
               IValidity(object).isValid(object) == False:
                continue                    
            
            if mtool.checkPermission("View", object) is not None:
                result.append(object)
        
        return result