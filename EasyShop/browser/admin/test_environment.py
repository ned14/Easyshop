# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.tests.utils import createTestEnvironment

class TestEnvironmentView(BrowserView):
    """
    """
    def create(self):
        """
        """
        portal = self.context
        createTestEnvironment(portal)
