# Five imports
from Products.Five.browser import BrowserView

# CMFPlone imports
from Products.CMFPlone import PloneMessageFactory as _

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IAddressManagement

class ManageAddressBookView(BrowserView):
    """
    """
    def deleteAddress(self):
        """
        """
        # delete address
        toDeleteAddressId = self.context.request.get("id")
        am = IAddressManagement(self.context)
        am.deleteAddress(toDeleteAddressId)
        
        # add message
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(_("The address has been deleted."))
                                        
        # redirect to addressbook
        url = "%s/manage-addressbook" % self.context.absolute_url()
        self.context.request.response.redirect(url)
            
