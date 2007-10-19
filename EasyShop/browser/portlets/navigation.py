# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICategoryManagement
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IProductContent
from Products.EasyShop.interfaces import ICategoryContent

class IPortletShopNavigationView(Interface):
    """
    """
    def getCategories():
        """
        """

    def showPortlet():
        """Returns True if the portlet is to be displayed.
        """   
        
    def showQuantity():
        """
        """

    def getShopUrl():
        """Returns the url to the parent shop
        """    
                    
    def showSubTree(context, category):
        """
        """

    def getStartingCategory():
        """Returns the top most parent object with which the navigation 
        starts.
        
        Could be use to start with a sub category. See Demmelhuber.
        """
        
    def getTopLevelCategories():
        """Returns the top level categories of the shop.
        """
        
class PortletShopNavigationView(BrowserView):
    """
    """
    implements(IPortletShopNavigationView)

    def getCategories(self):
        """
        """
        category = self.getStartingCategory()

        if category is None:
            return []
        else:    
            categories = ICategoryManagement(category).getTopLevelCategories()

            result = []
            for category in categories:
            
                result.append({
                    "klass"              : _getItemClass(self.context, category),
                    "url"                : category.getURL,
                    "description"        : category.Description,
                    "title"              : category.Title,
                    "amount_of_products" : category.total_amount_of_products,
                    "subcategories"      : _getSubCategories(self.context, category),
                    "show_subtree"       : _showSubTree(self.context, category),
                })

            return result 
                    
    def showPortlet(self):
        """
        """
        if ICategoryContent.providedBy(self.context) == False and \
           IProductContent.providedBy(self.context) == False:
            return False
        
        if ICategoryContent.providedBy(self.context):
            category = self.context
            
        elif IProductContent.providedBy(self.context):
            try:
                category = ICategoryManagement(self.context).getCategories()[0]
            except IndexError:
                return False
                 
        cm = ICategoryManagement(category)
        if cm.hasParentCategory() == False and cm.hasCategories() == False:
            return False
        
        return True

    def showQuantity(self):
        """
        """
        return self.context.getShop().getShowNavigationQuantity()
        
    def getShopUrl(self):
        """
        """
        shop = self.context.getShop()
        return shop.absolute_url()
        
    def getStartingCategory(self):
        """
        """
        # Could be use to show categories from a certain level on.
        # See demmelhuber
        return self.context.getShop()

    def getTopLevelCategories(self):
        """
        """
        shop = self.context.getShop()
        
        cm = ICategoryManagement(shop)
        return cm.getTopLevelCategories()
        
def _showSubTree(context, category):
    """Decides, whether a subtree of a category will be displayed or not.
    """
    shop = context.getShop()
    if shop.getExpandAll() == True:
        return True
            
    context_url  = context.absolute_url()
    category_url = category.getURL()

    if context_url.startswith(category_url) == True:
        return True  
                  
    # Todo: Use interface and implements            
    elif context.portal_type == "Product":
        cm = ICategoryManagement(context)
        try:
            product_category = cm.getCategories()[0]
        except IndexError:
            return False

        while product_category.portal_type == "Category":
            if product_category.UID() == category.UID():
                return True 
            product_category = product_category.aq_inner.aq_parent
    
    return False
                
def _getSubCategories(context, category):
    """
    """
    result = []
    
    # Use catalog search directly here for speed reasons. Using 
    # ICategoryManagement() would force me to get the object out of the brain.
    catalog = getToolByName(context, "portal_catalog")
    brains = catalog(portal_type="Category",
                     path = {"query" : category.getPath(),
                             "depth" : 1},
                     sort_on = "getObjPositionInParent")

    for category in brains:
                            
        result.append({
            "klass"              : _getItemClass(context, category),
            "url"                : category.getURL,
            "description"        : category.Description,
            "title"              : category.Title,
            "amount_of_products" : category.total_amount_of_products,
            "subcategories"      : _getSubCategories(context, category),
            "show_subtree"       : _showSubTree(context, category),
        })

    return result 
    
def _getItemClass(context, category):
    """Returns the css class of the category, which differs between current
    or not current.
    """
    context_url  = context.absolute_url()
    category_url = category.getURL()
    
    if context_url == category_url:
        return "navTreeCurrentItem visualIconPadding"
    elif context.portal_type == "Product":
        try:
            product_category =\
            context.getBRefs("easyshopcategory_easyshopproduct")[0]            
        except IndexError:
            return "visualIconPadding"
        
        # UID doesn't work here. Don't know why yet.
        if category.getPath() == "/".join(product_category.getPhysicalPath()):
            return "navTreeCurrentItem visualIconPadding"     
            
    return "visualIconPadding"