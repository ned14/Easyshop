from zope.i18n import translate
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.shop.utilities.misc import sendMultipartMail
from easyshop.core.config import _


class SendRecommendation(BrowserView):
    """
    """
    render = ViewPageTemplateFile('recommendation.pt')

    def __call__(self):
        """
        """
        utool = getToolByName(self.context, "plone_utils")

        if self.request.get("email", "") == "":
            utool.addPortalMessage(_("Please add a e-mail address."))
            url = "%s/thank-you" % self.context.absolute_url()
        else:
            # Get charset
            props = getToolByName(self.context,
                "portal_properties").site_properties
            charset = props.getProperty("default_charset")
            text = self.render()

            sendMultipartMail(
                context = self.context,
                sender = self.context.getMailFromAddress(),
                receiver = self.request.get("email"),
                subject = translate(_("EasyShop recommendation"),
                    target_language=self.request.get('LANGUAGE', 'de')),
                text = text,
                charset = charset)

            utool.addPortalMessage(_("Your mail has been sent."))
            url = "%s/thank-you" % self.context.absolute_url()

        self.request.response.redirect(url)

    def getMailInfo(self):
        """
        """
        cm = ICustomerManagement(self.context)
        sm = IShopManagement(self.context)
        shop = sm.getShop()
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        shipping_address = am.getShippingAddress()

        mtool = getToolByName(self.context, "portal_membership")
        member = mtool.getAuthenticatedMember()

        name = shipping_address.getFirstname() + " "
        name += shipping_address.getLastname()

        return dict(
            email=member.getProperty("email"),
            name=name,
            shop_title=shop.Title(),
            shop_url=shop.absolute_url())
