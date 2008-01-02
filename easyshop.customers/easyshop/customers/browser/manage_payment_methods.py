# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import IPaymentInformationManagement

class ManagePaymentMethodsView(BrowserView):
    """
    """
    def deletePaymentMethod(self):
        """
        """
        putils = getToolByName(self.context, "plone_utils")
        
        # delete address
        toDeletepPaymentMethodId = self.context.request.get("id")
        pm = IPaymentInformationManagement(self.context)
        pm.deletePaymentInformation(toDeletepPaymentMethodId)
        
        # add message
        putils.addPortalMessage("The payment method has been deleted.")
                                        
        # Redirect to overview
        url = "%s/manage-payment-methods" % self.context.absolute_url()
        self.context.request.response.redirect(url)
            
    def getDirectDebitAccounts(self):
        """
        """   
        pm  = IPaymentInformationManagement(self.context)
        return pm.getPaymentInformations(IBankAccount)
        
    def getCreditCards(self):
        """
        """   
        pm  = IPaymentInformationManagement(self.context)
        return pm.getPaymentInformations(ICreditCard)