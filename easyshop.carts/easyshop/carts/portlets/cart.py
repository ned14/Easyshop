# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# create message factory
_ = MessageFactory("EasyShop")

class ICartPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(ICartPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"Cart")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('cart.pt')

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
