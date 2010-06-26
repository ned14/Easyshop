# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IFormatterInfos
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices

from easyshop.shop.subscribers.mailing import sendMultipartMail

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
                
