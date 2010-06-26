# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop importss
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IProductGroup

class GroupProductManager:
    """
    """
    implements(IProductManagement)
    adapts(IProductGroup)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getProducts(self):
        """
        """       
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs('groups_products'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result
    
    def getAmountOfProducts(self):
        """
        """
        return len(self.getProducts())