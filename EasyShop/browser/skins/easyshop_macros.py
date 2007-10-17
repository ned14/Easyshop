# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICategoryManagement
from Products.EasyShop.interfaces import IProductManagement

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
        sorting = self.request.get("sorting", None)        
        try:
            sorted_on, sort_order = sorting.split("-")
        except (AttributeError, ValueError):
            sorted_on  = "price"
            sort_order = "desc"
        
        # all categories of the product
        cm = ICategoryManagement(self.context)
        categories = cm.getCategories()
        
        result = []
        for category in categories:
            pm = IProductManagement(category)
            products = pm.getAllProducts(sorted_on=sorted_on,
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
                temp["previous"] = "%s?sorting=%s" % (product.absolute_url(), sorting)
                temp["first"] = "%s?sorting=%s" % (products[0].absolute_url(), sorting)
            try:
                product = products[index+1]
                temp["next"] = "%s?sorting=%s" % (product.absolute_url(), sorting)
                temp["last"] = "%s?sorting=%s" % (products[-1].absolute_url(), sorting)
            except IndexError:
                temp["next"] = None
                temp["last"] = None

            temp["category"] = category.Title()
            temp["position"] = index + 1
            temp["amount"] = len(products)            
            
            result.append(temp)
            
        return result