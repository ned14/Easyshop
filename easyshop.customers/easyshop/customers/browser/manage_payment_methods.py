# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentManagement 
from easyshop.core.interfaces import IDirectDebit

class ManagePaymentMethodsView(BrowserView):
    """
    """
    def deletePaymentMethod(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        putils = getToolByName(self.context, "plone_utils")        
        
        # delete address
        toDeletepPaymentMethodId = self.context.request.get("id")
        pm = IPaymentManagement(customer)
        pm.deletePaymentMethod(toDeletepPaymentMethodId)
        
        # add message
        putils.addPortalMessage("The payment method has been deleted.")
                                        
        # Redirect to overview
        url = "%s/manage-payment-methods" % self.context.absolute_url()
        self.context.request.response.redirect(url)
            
    def getCustomer(self):
        """
        """
        cm = ICustomerManagement(self.context)
        return cm.getAuthenticatedCustomer()

    def getDirectDebitAccounts(self):
        """
        """   
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()

        pm  = IPaymentManagement(customer)
        return pm.getPaymentMethods(IDirectDebit)

