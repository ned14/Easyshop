# zope imports
from zope.component import adapter
from zope.component import getMultiAdapter

# utils imports
from Products.CMFCore.utils import getToolByName

# DCWorkflow imports
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

# easyshop imports
from easyshop.core.interfaces import IOrder
from easyshop.core.interfaces import IShopManagement
from easyshop.shop.utilities.misc import sendMultipartMail

@adapter(IOrder, IAfterTransitionEvent)
def sendOrderMail(order, event):
    """
    """
    state = event.new_state.getId()

    if state == "pending":
        mailOrderSubmitted(order)
        
    elif state in ("sent (not payed)", "sent"):
        mailOrderSent(order)

def mailOrderSent(order):
    """Sends email to customer that the order has been sent.
    """
    import pdb; pdb.set_trace()
    shop = IShopManagement(order).getShop()

    view = getMultiAdapter((order, order.request), name="mail-order-sent")
    text = view()
    
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

def mailOrderSubmitted(order):
    """Sends email to shop owner that an order has been submitted.
    """
    import pdb; pdb.set_trace()
    shop = IShopManagement(order).getShop()
    
    if shop.getMailFrom() and shop.getMailTo():
        view = getMultiAdapter((order, order.request), name="mail-order-submitted")
        text = view()

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