# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICategoryManagement

class ICategoriesView(Interface):    
    """
    """
    def getTopLevelCategories():
        """Returns the top level categories of the shop.
        """    
       
class CategoriesView(BrowserView):
    """
    """
    implements(ICategoriesView)

    def getTopLevelCategories(self):
        """
        """
        shop = self.context.getShop()
        
        cm = ICategoryManagement(shop)
        
        result = []
        for category in cm.getTopLevelCategories():
            result.append({
                "title"       : category.Title,
                "description" : category.Description,
                "url"         : category.getURL(),
            })
            
        return result
        
    
    