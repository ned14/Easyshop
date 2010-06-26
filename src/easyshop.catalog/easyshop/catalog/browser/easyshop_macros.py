# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement

# Todo: Find out how an macro could be a template of a view.
class INavigationMacroView(Interface):    
    """
    """
    def getProductURLs():
        """Returns the product urls.
        """
           
class NavigationMacroView(BrowserView):
    """
    """
    implements(INavigationMacroView)
    
    def getProductURLs(self):
        """
        """
        sorting = self.request.SESSION.get("sorting")
        try:
            sorted_on, sort_order = sorting.split("-")
        except (AttributeError, ValueError):
            sorted_on  = "price"
            sort_order = "desc"
        
        # all categories of the product
        cm = ICategoryManagement(self.context)
        categories = cm.getTopLevelCategories()
        
        result = []
        for category in categories:
            pm = IProductManagement(category)
            products = pm.getAllProducts(
                sorted_on=sorted_on,
                sort_order = sort_order)
            
            # determine position of product within category
            index = products.index(self.context)
            
            # generate previous/next url
            temp = {}            
            if index==0:
                temp["previous"] = None
                temp["first"] = None
            else:
                product = products[index-1]
                temp["previous"] = product.absolute_url()
                temp["first"] = products[0].absolute_url()
            try:
                product = products[index+1]
                temp["next"] = product.absolute_url()
                temp["last"] = products[-1].absolute_url()
            except IndexError:
                temp["next"] = None
                temp["last"] = None

            temp["category_url"] = category.absolute_url()
            temp["category"] = category.Title()
            temp["position"] = index + 1
            temp["amount"] = len(products)            
            
            result.append(temp)
            
        return result