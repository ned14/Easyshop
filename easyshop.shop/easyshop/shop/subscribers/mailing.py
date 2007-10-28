# utils imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

# email imports
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email import Encoders

def sendMultipartMail(context, from_, to, cc=[], bcc=[], subject="", text="", charset="utf-8"):
    """
    """
    mail = MIMEMultipart("alternative")
        
    mail['From']    = from_
    mail['To']      = to
    mail['Bcc']     = "".join(cc)
    mail['Bcc']     = "".join(bcc)
    mail['Subject'] = subject
    mail.epilogue   = ''

    # create & attach text part 
    text = text.encode("utf-8")
    text_part = MIMEText(text, "plain", charset)
    mail.attach(text_part)

    # create & attach html part with images            
    html_part = MIMEMultipart("related")
    html_code = MIMEText(text, "html", charset)            
    html_part.attach(html_code)       
    mail.attach(html_part)

    context.MailHost.send( mail.as_string() )
    # except:
    #     # catch and do nothing, so that the user doesn't notice an error
    #     pass
        
def mailOrderSubmitted(event):
    """Sends email to notify that an order has been submitted.
    """
    # Todo: Check possibility of TemplateFields, especially ZPTField in 
    # another context as the field owner.
    order = event.context
    shop = order.IShopManagement(order).getShop()
    
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
