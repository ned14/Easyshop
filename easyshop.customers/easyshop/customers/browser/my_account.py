# Five imports
from Products.Five.browser import BrowserView

# EasyShop Products
from easyshop.core.interfaces import ICustomerManagement

class MyAccountView(BrowserView):
    """
    """
    def getCustomerEditURL(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        return "%s/@@edit" % customer.absolute_url()