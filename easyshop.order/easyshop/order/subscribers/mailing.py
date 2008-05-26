# zope imports
from zope.component import adapter
from zope.component import getMultiAdapter

# utils imports
from Products.CMFCore.utils import getToolByName

# DCWorkflow imports
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IMailAddresses
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
        mailOrderReceived(order)
        
    elif state in ("sent (not payed)", "sent"):
        mailOrderSent(order)

def mailOrderSent(order):
    """Sends email to customer that the order has been sent.
    """
    shop = IShopManagement(order).getShop()

    # Get mail content
    view = getMultiAdapter((order, order.REQUEST), name="mail-order-sent")
    text = view()

    # Get customer
    customer = order.getCustomer()

    # Get charset
    props = getToolByName(order, "portal_properties").site_properties
    charset = props.getProperty("default_charset")

    # Get sender
    sender = IMailAddresses(shop).getSender()
    
    sendMultipartMail(
        context  = order,
        sender   = sender,
        receiver = customer.email,
        subject  = "Your order %s has been sent." % order.getId(),
        text     = text,
        charset  = charset)

def mailOrderSubmitted(order):
    """Sends email to shop owner that an order has been submitted.
    """
    shop = IShopManagement(order).getShop()

    # Get sender and receiver
    mail_addresses = IMailAddresses(shop)
    sender    = mail_addresses.getSender()
    receivers = mail_addresses.getReceivers()

    if sender and receivers:
        view = getMultiAdapter((order, order.REQUEST), name="mail-order-submitted")
        text = view()

        # get charset
        props = getToolByName(order, "portal_properties").site_properties
        charset = props.getProperty("default_charset")

        sendMultipartMail(
            context  = order,
            sender   = sender,
            receiver = ", ".join(receivers),
            subject  = "E-Shop: New order",
            text     = text,
            charset  = charset)
            
def mailOrderReceived(order):
    """Sends email to customer that the order has been received.
    """
    shop = IShopManagement(order).getShop()

    # Get sender
    mail_addresses = IMailAddresses(shop)
    sender         = mail_addresses.getSender()
    bcc            = mail_addresses.getReceivers()
    
    # Get receiver
    customer = order.getCustomer()
    address = IAddressManagement(customer).getShippingAddress()
    receiver = address.email
    
    if sender and receiver:
        view = getMultiAdapter((order, order.REQUEST), name="mail-order-received")
        text = view()

        # get charset
        props = getToolByName(order, "portal_properties").site_properties
        charset = props.getProperty("default_charset")

        sendMultipartMail(
            context  = order,
            sender   = sender,
            receiver = receiver,
            bcc      = bcc,
            subject  = "Bestellbestätigung Demmelhuber Holz & Raum",
            text     = text,
            charset  = charset)