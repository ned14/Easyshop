# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMF imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProduct

class ProductGroupManagement:
    """Provides IGroupManagement for product content objects.
    """
    implements(IGroupManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def hasGroups(self):
        """
        """
        if len(self.getGroups()) > 0:
            return True
        return False

    def getGroups(self):
        """
        """       
        # Need this here, because the shipping product is a temporary product 
        # and has no context and could not get reference_catalog
        try:
            return self.context.getBRefs("groups_products")
        except AttributeError:
            return []
