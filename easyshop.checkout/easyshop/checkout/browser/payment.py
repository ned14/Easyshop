# Zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IDirectDebit
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IShopPaymentMethod
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class ICheckOutPaymentView(Interface):    
    """Provides methods for all payment forms
    (Which are all in context of a shop content object)
    """    

    def getDirectDebits():
        """Returns all direct debits of authenticated customer.
        """    

    def getSelectedPaymentMethod():
        """Returns selected payment method of authenticated customer.
        """

    def getShopPaymentMethods():
        """Returns all shop payment content objects.
        """

    def isDirectDebitValid(self):
        """Returns True if direct debit is a valid payment method.
        """        
        
class CheckOutPaymentView(BrowserView):
    """
    """
    implements(ICheckOutPaymentView)

    def getDirectDebits(self):
        """
        """
        if self.isDirectDebitValid() == False:
            return []
        
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        result = []        
        pm = IPaymentManagement(customer)    
        for direct_debit in pm.getPaymentMethods(
            interface=IDirectDebit, check_validity=True):
            
            selected_payment_method = pm.getSelectedPaymentMethod(check_validity=True)
            if selected_payment_method.getId() == direct_debit.getId():
                checked = True
            else:
                checked = False            
            
            result.append({
                "id"         : direct_debit.getId(),
                "bic"        : direct_debit.getBankIdentificationCode(),
                "account_no" : direct_debit.getAccountNumber(),
                "name"       : direct_debit.getName(),
                "bankname"   : direct_debit.getBankName(),
                "checked"    : checked,
            })
        
        return result

    def getSelectedPaymentMethod(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        pm = IPaymentManagement(customer)
        return pm.getSelectedPaymentMethod(check_validity=True)
        
    def getShopPaymentMethods(self):
        """
        """        
        shop = IShopManagement(self.context).getShop()
        spm = IPaymentManagement(shop)
        selected_payment = spm.getSelectedPaymentMethod(check_validity=True)                
        result = []
        for payment in spm.getPaymentMethods(
            interface=IShopPaymentMethod, check_validity=True):

            # Todo: Make default payment method editable. ATM it is prepayment.
            # So if nothing is selected checked is true for prepayment.

            # If id is direct_debit_new (this happens when customer wants to 
            # add a new direct debit and is due to validation errors redirected to 
            # the form.
            
            # TODO: This has to be more tested and optimized

            if self.request.get("id", "") == "direct_debit_new":
                checked = False                
            elif selected_payment.getId() == payment.getId() or\
               selected_payment == "":
               checked = True
            else:
                checked = False
                
            result.append({                
                "id"          : payment.getId(),
                "title"       : payment.Title(),
                "description" : payment.Description(),               
                "checked"     : checked,
            })
        
        return result

    def isDirectDebitValid(self):
        """
        """
        # This decides whether the form for new direct debit is to be
        # displayed or not.
        spm = IPaymentManagement(IShopManagement(self.context).getShop())
        dd = spm.getPaymentMethod("direct-debit")
        
        if dd is None or IValidity(dd).isValid() == False:
            return False
        else:
            return True