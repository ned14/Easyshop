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
        text = []

        for key, value in self.request.form.items():
            if key == "receiver":
                continue
            text.append("%s: %s" % (key, value))

        text = "\n".join(text)

        portal = getToolByName(self.context,'portal_url').getPortalObject()
        sender = portal.email_from_address
        receiver = self.request.get("receiver", sender)
        
        subject = "Neue Nachricht von %s" % portal.Title()
        sendNonMultipartMail(self.context, sender=sender, receiver=receiver, subject=subject, text=text)
        
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage("Wir haben Ihre Mail empfangen. Vielen Dank!")
        
        url = self.context.absolute_url()
        self.context.request.response.redirect(url)
        
