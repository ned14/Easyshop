# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerContent
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IPaymentMethodContent
from Products.EasyShop.interfaces import IValidity

class CustomerPaymentManager:
    """
    """
    implements(IPaymentManagement)
    adapts(ICustomerContent)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def deletePaymentMethod(self, id):
        """
        """
        try:    
            self.context.manage_delObjects(id)
        except AttributeError:
            return False

            # Shop level methods shouldn't deleted here. So we do nothing
            # here. Contrary to the other methods below which go also on shop 
            # level
            
        return True

    def getPaymentMethod(self, id):
        """Returns payment method by given id.
        """
        try:
            return self.context[id]
        except KeyError:
            return None
                    
    def getPaymentMethods(self, interface=None, check_validity=False):
        """Returns the payment methods of a customer. 
        """
        # Todo: This can be optimized with Plone 3.0 because there will be an
        # interface index (IIRC).
        
        if interface is None:
            interface = IPaymentMethodContent        

        result = []
        for object in self.context.objectValues():

            if interface.providedBy(object) == False:
                continue
                
            if check_validity == True and\
               IValidity(object).isValid(object) == False:
                continue                    

            result.append(object)
                
        return result        
        
    def getSelectedPaymentMethod(self, check_validity=False):
        """
        """
        # First try to get the payment method on customer level. If it isn't
        # found, get it from shop level. (If it isn't found there, which
        # should never happen returns the default method; see shop/payment
        # for more information.)
        
        try:
            selected_method = getattr(
                self.context, 
                self.context.getSelectedPaymentMethod())
                
        except AttributeError:
            shop = self.context.getShop()
            pm = IPaymentManagement(shop)
            selected_method = pm.getSelectedPaymentMethod()
        
        # if selected payment method is not valid return default
        # Todo: Make default manageable    
        if check_validity == False:
            return selected_method
        else:
            if IValidity(selected_method).isValid() == False:
                shop = self.context.getShop()
                pm = IPaymentManagement(shop)
                return pm.getSelectedPaymentMethod(check_validity)
            else:
                return selected_method

    def getSimplePaymentMethods(self, check_validity=False):
        """Get simple payment content objects.
        """
        return []