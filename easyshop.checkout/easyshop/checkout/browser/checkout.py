# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.core imports
from easyshop.core.interfaces import ICheckoutManagement

class CheckoutView(BrowserView):
    """
    """
    def checkout(self):
        """The start of the checkout process.
        """   
        mtool = getToolByName(self.context, "portal_membership")
        ICheckoutManagement(self.context).redirectToNextURL("AFTER_START")