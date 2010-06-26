from zope.component import getMultiAdapter
# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement

class SendRecommendationView(BrowserView):
    """
    """
    def getMailInfo(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        shipping_address = am.getShippingAddress()

        mtool = getToolByName(self.context, "portal_membership")        
        member = mtool.getAuthenticatedMember()
        
        name  = shipping_address.getFirstname() + " "
        name += shipping_address.getLastname()
                
        return {
            "email" : member.getProperty("email"),
            "name"  : name,
        }
                
    def portal_url(self):
        portal_state = getMultiAdapter((self.context,self.request),
                                       name="plone_portal_state")
        return portal_state.portal_url()
