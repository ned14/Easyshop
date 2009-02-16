# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IProduct

class ILastSeenPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(ILastSeenPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Last Seen")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('last_seen.pt')

    @property
    def available(self):
        """
        """
        return len(self.getLastSeenProducts()) > 0
    
    @memoize
    def getLastSeenProducts(self):
        """
        """
        result = []
        for product in self.request.SESSION.get("last_products", []):
            if product["url"] != self.context.absolute_url():
                result.append(product)
        return result
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()