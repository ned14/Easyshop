# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# EasyShop imports
from Products.EasyShop.config import _
from Products.EasyShop.interfaces import ICategory
from Products.EasyShop.interfaces import IProduct

class ISortingPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(ISortingPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Sorting")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('sorting.pt')

    @property
    def available(self):
        """
        """
        return True
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()