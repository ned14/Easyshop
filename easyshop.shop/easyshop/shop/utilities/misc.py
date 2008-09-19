# CMFCore imports
from Products.CMFCore.utils import getToolByName

# email imports
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMENonMultipart import MIMENonMultipart
from email.Utils import COMMASPACE, formatdate
from email.MIMEBase import MIMEBase
from email import Encoders

# TODO: Move this to a local utility
def getObjectByUID(context, uid):
    """
    """
    catalog = getToolByName(context, "portal_catalog")
    brains = catalog.searchResults(
        uid = uid
    )
    
    try:
        return brains[0]
    except IndexError:
        return None
        
def sendMultipartMail(context, sender, receiver, cc=[], bcc=[], subject="", text="", charset="utf-8"):
    """
    """
    mail = MIMEMultipart("alternative")
        
    mail['From']    = sender
    mail['To']      = receiver
    mail['Cc']     = ", ".join(cc)
    mail['Bcc']     = ", ".join(bcc)
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

    context.MailHost.send(mail.as_string())
        
def sendNonMultipartMail(context, sender, receiver, cc=[], bcc=[], subject="", text="", charset="utf-8"):
    """
    """
    mail = MIMENonMultipart("text", "plain")

    mail['From']    = sender
    mail['To']      = receiver
    mail['Cc']      = ", ".join(cc)
    mail['Bcc']     = ", ".join(bcc)
    mail['Subject'] = subject

    text = text.encode("utf-8")
    mail.set_payload(text)
    
    context.MailHost.send(mail.as_string())
    
    
def sendMailWithAttachements(context, sender, receiver, cc=[], bcc=[], subject="", text="", files=[]):
    """
    """
    mail = MIMEMultipart()
    
    mail['From'] = sender
    mail['To']  = receiver
    mail['Cc'] = COMMASPACE.join(cc)
    mail['Bcc'] = COMMASPACE.join(bcc)        
    mail['Subject'] = subject
    
    # text = text.encode("utf-8")
    # text_part = MIMEText(text, "plain", "utf-8")
    # mail.attach(text_part)

    # create & attach html part with images
    text = text.encode("utf-8")
    mail.attach(MIMEText(text, "html", "utf-8"))
    
    for filename, file_ in files:
        try:
            data = file_.data.data
        except AttributeError:
            data = file_.data
            
        attachment_part = MIMEBase('application', "octet-stream")
        attachment_part.set_payload(data)
        Encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', 'attachment; filename=%s' % filename)
        mail.attach(attachment_part)
    
    context.MailHost.send(mail.as_string())