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
from easymall.mall.interfaces import IMallManagement

class IMallAdminPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IMallAdminPortlet)

    def __init__(self):
        """
        """
    @property
    def title(self):
        """
        """
        return _(u"EasyMall Manager")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('mall_admin.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        else:
            return False

    def getMallURL(self):
        """
        """
        return IMallManagement(self.context).getMall().absolute_url()
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()