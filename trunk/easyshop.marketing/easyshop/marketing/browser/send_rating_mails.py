# python imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IMailAddresses
from easyshop.shop.utilities.misc import sendMultipartMail

class SendRatingMailsView(BrowserView):
    """Sends email to customer to rate buyed products.
    """
    def send_rating_mails(self):
        """
        """
        now = DateTime()
        
        # Get sender
        mail_addresses = IMailAddresses(self.context)        
        sender         = mail_addresses.getSender()
        bcc            = ["kai.diefenbach@iqpp.de"]

        # Get all relevant orders
        om = IOrderManagement(self.context)
        
        for order in om.getOrders():
            
            if "rating-mail" in order.getMarketingInfo():
                continue
            
            # Send only mails for orders which are older than 6 weeks
            # difference in days (6 weeks)
            if now - order.created() < (6*7):
                continue

            import pdb; pdb.set_trace()
                                                
            # Get receiver
            customer = order.getCustomer()
            address = IAddressManagement(customer).getShippingAddress()
            receiver = address.email
    
            if sender and receiver:
                view = getMultiAdapter((order, order.REQUEST), name="rating-mail")
                text = view()
                                
                # get charset
                props = getToolByName(order, "portal_properties").site_properties
                charset = props.getProperty("default_charset")
                
                sendMultipartMail(
                    context  = order,
                    sender   = sender,
                    receiver = "kai.diefenbach@iqpp.de",
                    bcc      = bcc,
                    subject  = "Bewerten Sie Ihr Produkt",
                    text     = text,
                    charset  = charset)
                    
                # set marketing info
                mi = list(order.getMarketingInfo())
                mi.append("rating-mail")
                order.setMarketingInfo(mi)