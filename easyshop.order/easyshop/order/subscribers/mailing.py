# utils imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShopManagement
from easyshop.shop.utilities.misc import sendMultipartMail

def mailOrderSubmitted(event):
    """Sends email to notify that an order has been submitted.
    """
    # Todo: Check possibility of TemplateFields, especially ZPTField in 
    # another context as the field owner.
    order = event.context
    shop = IShopManagement(order).getShop()
    
    if shop.getMailFrom() and shop.getMailTo():
        text = order.mail_order_submitted()

        # get charset
        props = getToolByName(order, "portal_properties").site_properties
        charset = props.getProperty("default_charset")

        sendMultipartMail(
            context = order,
            from_   = shop.getMailFrom(),
            to      = ", ".join(shop.getMailTo()),
            subject = "E-Shop: New order",
            text    = text,
            charset = charset)
        
def mailOrderSent(event):
    """Sends email to notify that an order has been sent.
    """
    # Todo: Check possibility of TemplateFields, especially ZPTField in 
    # another context as the field owner.
    order = event.context
    shop = IShopManagement(order).getShop()

    text = order.mail_order_sent()
    
    mtool = getToolByName(order, "portal_membership")
    member = mtool.getAuthenticatedMember()    

    # get charset
    props = getToolByName(order, "portal_properties").site_properties
    charset = props.getProperty("default_charset")
        
    sendMultipartMail(
        context = order,    
        from_   = shop.getMailFrom(),
        to      = member.getProperty("email"),
        subject = "Your order %s has been sent." % order.getId(),
        text    = text,
        charset = charset)
