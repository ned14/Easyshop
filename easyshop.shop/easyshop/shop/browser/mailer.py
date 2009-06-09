# plone imports
from plone.memoize.instance import memoize

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.shop.utilities.misc import sendNonMultipartMail

class FormView(BrowserView):
    """
    """
    def sendForm(self):
        """
        """
        text = "\n".join(self.request.form.items())            
        sender = "info@demmelhuber.net"
        receiver = "usenet@diefenba.ch"
        subject = "Form"        
        sendNonMultipartMail(self.context, sender=sender, receiver=receiver, subject=subject, text=text)
