# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentMethod
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class CustomerPaymentManager:
    """
    """
    implements(IPaymentManagement)
    adapts(ICustomer)
    
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
        mtool = getToolByName(self.context, "portal_membership")
            
        if interface is None:
            interface = IPaymentMethod        

        result = []
        for object in self.context.objectValues():

            if interface.providedBy(object) == False:
                continue
                
            if check_validity == True and\
               IValidity(object).isValid(object) == False:
                continue                    

            if mtool.checkPermission("View", object) is not None:
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
            self.context[self.context.selected_payment_method]                 
        except KeyError:
            shop = IShopManagement(self.context).getShop()
            pm = IPaymentManagement(shop)
            selected_method = pm.getSelectedPaymentMethod()
        
        # if selected payment method is not valid return default
        # Todo: Make default manageable    
        if check_validity == False:
            return selected_method
        else:
            if IValidity(selected_method).isValid() == False:
                shop = IShopManagement(self.context).getShop()
                pm = IPaymentManagement(shop)
                return pm.getSelectedPaymentMethod(check_validity)
            else:
                return selected_method

    def getSimplePaymentMethods(self, check_validity=False):
        """Get simple payment content objects.
        """
        return []