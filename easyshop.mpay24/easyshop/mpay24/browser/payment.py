from base64 import decodestring
from urllib import unquote

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.mpay24.config import REDIR_COOKIE_NAME
from easyshop.checkout.browser.thank_you import ThankYouPageView as \
    ThankYouPageViewBase

class ThankYouPageView(ThankYouPageViewBase):
    """
    """

    def mpay24_redirect_url(self):
        """
        """
        redir_url = decodestring(
            unquote(self.request.get(REDIR_COOKIE_NAME,''))
        )

        if not redir_url:
            return

        return unquote(redir_url)