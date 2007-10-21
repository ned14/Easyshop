# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import ICategoryManagement
from Products.EasyShop.interfaces import ICategory
from Products.EasyShop.interfaces import IPrices

class CategoryProductManager:
    """An adapter which provides IProductManagement for category content
    objects.
    """
    implements(IProductManagement)
    adapts(ICategory)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getProducts(self, category_id=None):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs('easyshopcategory_easyshopproduct'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result

    def getAllProducts(self, sorted_on=None, sort_order=None):
        """
        """
        pm = IProductManagement(self.context)
        products = pm.getProducts()
        
        cm = ICategoryManagement(self.context)
        for category in cm.getTotalCategories():
            pm = IProductManagement(category)
            products.extend(pm.getProducts())
            
        if sorted_on == "name":
            products = sortProductsByName(products, sort_order)
        elif sorted_on == "price":
            products = sortProductsByPrice(products, sort_order)                        

        return products
        
    def getAmountOfProducts(self):
        """
        """
        return len(self.getProducts())

    def getTotalAmountOfProducts(self):
        """
        """
        return len(self.getAllProducts())
        

def sortProductsByName(products, order=None):
    """
    """
    if order == "desc":
        products.sort(lambda a, b: cmp(b.Title(), a.Title()))
    else:
        products.sort(lambda a, b: cmp(a.Title(), b.Title()))                
        
    return products
    
def sortProductsByPrice(products, order=None):
    """
    """
    if order == "desc":
        products.sort(lambda a, b: cmp(IPrices(b).getPriceGross(), IPrices(a).getPriceGross()))
    else:
        products.sort(lambda a, b: cmp(IPrices(a).getPriceGross(), IPrices(b).getPriceGross()))
        
    return products      