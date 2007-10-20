# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop importss
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IGroupContent

class GroupProductManager:
    """
    """
    implements(IProductManagement)
    adapts(IGroupContent)
    
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
        for product in self.context.getRefs('easyshopgroup_easyshopproduct'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result
    
    def getAmountOfProducts(self):
        """
        """
        return len(self.getProducts())