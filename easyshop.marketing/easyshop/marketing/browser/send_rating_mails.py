# python imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IMailAddresses
from easyshop.core.interfaces import IOrderManagement

from easyshop.shop.utilities.misc import sendMultipartMail

class SendRatingMailsView(BrowserView):
    """Sends email to customer to rate buyed products.
    """
    def send_rating_mails(self):
        """
        """
        live = self.request.get("live")
        
        now = DateTime()
        
        # Get sender
        mail_addresses = IMailAddresses(self.context)
        sender         = mail_addresses.getSender()
        bcc            = ["kai.diefenbach@iqpp.de"]
        
        wftool = getToolByName(self.context, "portal_workflow")
        
        # Get all relevant orders
        om = IOrderManagement(self.context)
        
        for order in om.getOrders():
            
            # Send mail only once (below "rating-mail" is set)
            if "rating-mail" in order.getMarketingInfo():
                continue

            # Send mail only for closed orders
            if wftool.getInfoFor(order, "review_state") != "closed":
                continue
                            
            # Send only mails for orders which are older than 2 weeks
            # difference in days
            if now - order.created() < (2*7):
                continue
            
            # Send only mails for orders which have at least on product with 
            # a valid url (aka product which is not deleted in the meanwhile)
            if self.hasItems(order) == False:
                continue
            
            if live is None:
                receiver = "usenet@diefenba.ch, d.kommol@demmelhuber.net"
                if sender and receiver:
                    view = getMultiAdapter((order, order.REQUEST), name="rating-mail")
                    text = view()
                                
                    # get charset
                    props = getToolByName(order, "portal_properties").site_properties
                    charset = props.getProperty("default_charset")
                
                    sendMultipartMail(
                        context  = order,
                        sender   = sender,
                        receiver = receiver,
                        subject  = "Bitte bewerten Sie Ihr Produkt",
                        text     = text,
                        charset  = charset)                    
            else:
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
                        receiver = receiver,
                        bcc      = bcc,
                        subject  = "Bitte bewerten Sie Ihr Produkt",
                        text     = text,
                        charset  = charset)
                    
                    # set marketing info
                    mi = list(order.getMarketingInfo())
                    mi.append("rating-mail")
                    order.setMarketingInfo(mi)
                
    def hasItems(self, order):
        """Returns True if order has at least one item with valid url
        """
        for item in IItemManagement(order).getItems():
            if item.getProduct() is not None:
                return True

        return False