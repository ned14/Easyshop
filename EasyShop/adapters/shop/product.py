# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IShopContent

class ProductManagement:
    """An adapter, which provides product management for shop content objects.
    """
    implements(IProductManagement)
    adapts(IShopContent)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getAllProducts(self):
        """
        """
        raise Exception
        
    def getAmountOfProducts(self):
        """
        """        
        raise Exception
        
    def getProducts(self):
        """
        """
        raise Exception
        
    def getTotalAmountOfProducts(self):
        """
        """
        raise Exception
