# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from iqpp.easyshop.config import _
from iqpp.easyshop.interfaces import ICategory
from iqpp.easyshop.interfaces import IProduct

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

# Five imports
from Products.Five.browser import BrowserView

class SortingPortletView(BrowserView):
    """
    """ 
    def setSorting(self):
        """
        """
        sorting = self.request.get("sorting")
        self.request.SESSION["sorting"] = sorting
        
        url = self.context.absolute_url()
        self.request.response.redirect(url)