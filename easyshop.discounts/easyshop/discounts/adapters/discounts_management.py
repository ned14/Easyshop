# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from iqpp.easyshop.interfaces import IDiscountsManagement
from iqpp.easyshop.interfaces import IShop
from iqpp.easyshop.interfaces import IValidity

class DiscountsManagement:
    """An adapter which provides IDiscountsManagement for shop content objects.
    """    
    implements(IDiscountsManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.discounts = self.context.discounts
        
    def getDiscounts(self):
        """Returns all existing discounts.
        """
        return self.discounts.objectValues()