# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IDirectDebit
from easyshop.core.interfaces import IPaymentManagement 

class ManagePaymentMethodsView(BrowserView):
    """
    """
    def deletePaymentMethod(self):
        """
        """
        putils = getToolByName(self.context, "plone_utils")
        
        # delete address
        toDeletepPaymentMethodId = self.context.request.get("id")
        pm = IPaymentManagement(self.context)
        pm.deletePaymentMethod(toDeletepPaymentMethodId)
        
        # add message
        putils.addPortalMessage("The payment method has been deleted.")
                                        
        # Redirect to overview
        url = "%s/manage-payment-methods" % self.context.absolute_url()
        self.context.request.response.redirect(url)
            
    def getDirectDebitAccounts(self):
        """
        """   
        pm  = IPaymentManagement(self.context)
        return pm.getPaymentMethods(IDirectDebit)
        
    def getCreditCards(self):
        """
        """   
        pm  = IPaymentManagement(self.context)
        return pm.getPaymentMethods(ICreditCard)