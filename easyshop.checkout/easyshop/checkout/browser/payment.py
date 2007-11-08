# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IDirectDebit
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IShopPaymentMethod
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class PaymentForm(BrowserView):
    """
    """

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
            
    def test(self, a, b, c):
        """
        """
        return False
        
    def selectPaymentMethod(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        
        name = self.request.get("name", "")
        account_number = self.request.get("account_number", "")
        bank_identification_code = self.request.get("bank_identification_code", "")
        bankname = self.request.get("bankname", "")
        
        id = self.request.get("id")
        if id.startswith("direct_debit_new"):
            # add DirectDebit
            id = self.context.generateUniqueId("DirectDebit")
            customer.invokeFactory("DirectDebit", id=id, title=name)
            direct_debit = getattr(customer, id)        
            direct_debit.setAccountNumber(account_number)
            direct_debit.setBankIdentificationCode(bank_identification_code)
            direct_debit.setBankName(bankname)
            direct_debit.setName(name)
        elif id.startswith("direct_debit_existing"):
            id = id.split(":")[1]

        customer.selectedPaymentMethod = id
        
        cm = ICheckoutManagement(self.context)
        cm.redirectToNextURL("SELECTED_PAYMENT_METHOD")        