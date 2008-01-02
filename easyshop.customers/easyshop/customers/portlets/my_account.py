# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.interface import Interface

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

# create message factory
_ = MessageFactory("EasyShop")

class IMyAccountPortletView(Interface):
    """
    """
    def available():
        """
        """
    def getMyAccountUrl():
        """
        """

    def getPortalUrl():
        """
        """

    def getUserName():
        """
        """

    def isAnonymous():
        """
        """

    def getCustomer():
        """
        """
        
class MyAccountPortletView(BrowserView):
    """
    """
    implements(IMyAccountPortletView)

    @property
    def available(self):
        """
        """
        return True

    @memoize
    def getMyAccountUrl(self):
        """
        """
        customer = self.getCustomer()
        return "%s/my-account" % customer.absolute_url()

    @memoize
    def getPortalUrl(self):
        """
        """
        utool = getToolByName(self.context, "portal_url")
        return utool.getPortalObject().absolute_url()

    @memoize
    def getUserName(self):
        """
        """
        customer = self.getCustomer()
        return customer.Title()

    @memoize
    def isAnonymous(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        return mtool.isAnonymousUser()

    @memoize
    def getCustomer(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return ICustomerManagement(shop).getAuthenticatedCustomer()