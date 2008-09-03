# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# create message factory
_ = MessageFactory("EasyShop")

# easyshop imports
from easyshop.core.interfaces import IShopManagement

class IAdminPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IAdminPortlet)

    def __init__(self):
        """
        """
    @property
    def title(self):
        """
        """
        return _(u"EasyShop Manager")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('admin.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        else:
            return False

    def getShopURL(self):
        """
        """
        return IShopManagement(self.context).getShop().absolute_url()
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()