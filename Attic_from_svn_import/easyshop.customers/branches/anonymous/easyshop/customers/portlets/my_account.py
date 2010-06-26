# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

# create message factory
_ = MessageFactory("EasyShop")

class IMyAccountPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IMyAccountPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"My Account")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('my_account.pt')

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
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()
