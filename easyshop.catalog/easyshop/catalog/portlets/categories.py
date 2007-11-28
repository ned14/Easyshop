# zope imports
from zope import schema
from zope.formlib import form
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShopManagement

class ICategoriesPortlet(IPortletDataProvider):
    """
    """
    expand_all = schema.Bool(
        title=_(u'Expand all'),
        description=_(u'If selected all categories are expanded by default.'),
        required=False,
        default=False,)

    show_quantity = schema.Bool(
        title=_(u'Show quantity'),
        description=_(u'If selected amount of product per categories is displayed.'),
        required=False,
        default=False,)


class Assignment(base.Assignment):
    """
    """
    implements(ICategoriesPortlet)

    def __init__(self, expand_all=False, show_quantity=False):
        """
        """
        self.expand_all = expand_all
        self.show_quantity = show_quantity
        
    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Categories")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('categories.pt')

    @property
    def available(self):
        """
        """
        return True
        
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
                    "klass"              : self._getItemClass(self.context, category),
                    "url"                : category.getURL,
                    "description"        : category.Description,
                    "title"              : category.Title,
                    "amount_of_products" : category.total_amount_of_products,
                    "subcategories"      : self._getSubCategories(self.context, category),
                    "show_subtree"       : self._showSubTree(self.context, category),
                })

            return result 
                    
    def showQuantity(self):
        """
        """
        return self.data.show_quantity
        
    def getShopUrl(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return shop.absolute_url()
        
    def getStartingCategory(self):
        """
        """
        # Could be use to show categories from a certain level on.
        # See demmelhuber
        return IShopManagement(self.context).getShop()

    def getTopLevelCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        
        cm = ICategoryManagement(shop)
        return cm.getTopLevelCategories()

    def _showSubTree(self, category):
        """Decides, whether a subtree of a category will be displayed or not.
        """
        if self.data.expand_all == True:
            return True
            
        context_url  = context.absolute_url()
        category_url = category.getURL()

        if context_url.startswith(category_url) == True:
            return True  
                  
        # Todo: Use interface and implements            
        elif context.portal_type == "Product":
            cm = ICategoryManagement(context)
            try:
                product_category = cm.getTopLevelCategories()[0]
            except IndexError:
                return False
            
            while product_category.portal_type == "Category":
                if product_category.UID() == category.UID:
                    return True 
                product_category = product_category.aq_inner.aq_parent
    
        return False

    def _getSubCategories(self, context, category):
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
                "klass"              : self._getItemClass(context, category),
                "url"                : category.getURL,
                "description"        : category.Description,
                "title"              : category.Title,
                "amount_of_products" : category.total_amount_of_products,
                "subcategories"      : self._getSubCategories(context, category),
                "show_subtree"       : self._showSubTree(context, category),
            })

        return result 
    
    def _getItemClass(self, context, category):
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
                context.getBRefs("category_products")[0]            
            except IndexError:
                return "visualIconPadding"
        
            # UID doesn't work here. Don't know why yet.
            if category.getPath() == "/".join(product_category.getPhysicalPath()):
                return "navTreeCurrentItem visualIconPadding"     
            
        return "visualIconPadding"
        
class AddForm(base.AddForm):
    """
    """
    def create(self, data):
        """
        """
        return Assignment(
            expand_all = data.get("expand_all", False),
            show_quantity = data.get("show_quantity", False),
        )
        
class EditForm(base.EditForm):
    """
    """
    form_fields = form.Fields(ICategoriesPortlet)
    label = _(u"Edit EasyShop Categories Portlet")
    description = _(u"This portlet displays the categories of an EasyShop.")