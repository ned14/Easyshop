# zope imports
from zope import schema
from zope.formlib import form
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

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
                
                show_subtree = self._showSubTree(category)
                
                if show_subtree == True:
                    klass = "navTreeCurrentItem visualIconPadding"
                else:
                    klass = "visualIconPadding"

                if show_subtree == True:
                    sub_categories = self._getSubCategories(category)
                else:
                    sub_categories = []
                    
                result.append({
                    "klass"              : klass,
                    "url"                : category.getURL,
                    "description"        : category.Description,
                    "title"              : category.Title,
                    "amount_of_products" : category.total_amount_of_products,
                    "subcategories"      : sub_categories,
                    "show_subtree"       : show_subtree,
                })

            return result 
                                        
    def showQuantity(self):
        """
        """
        return self.data.show_quantity
        
    def getShopUrl(self):
        """
        """
        shop = self._getShop()
        return shop.absolute_url()
        
    def getStartingCategory(self):
        """
        """
        # Could be use to show categories from a certain level on.
        # See demmelhuber
        return self._getShop()

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
            
        context_url  = self.context.absolute_url()
        category_url = category.getURL()

        if context_url.startswith(category_url) == True:
            return True  
                  
        # Todo: Use interface and implements            
        elif self.context.portal_type == "Product":
            cm = ICategoryManagement(self.context)
            try:
                product_category = cm.getTopLevelCategories()[0]
            except IndexError:
                return False
            
            while product_category.portal_type == "Category":
                if product_category.UID() == category.UID:
                    return True
                product_category = product_category.aq_inner.aq_parent
    
        return False

    def _getSubCategories(self, category):
        """
        """
        result = []
    
        # Use catalog search directly here for speed reasons. Using 
        # ICategoryManagement() would force me to get the object out of the brain.
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(portal_type="Category",
                         path = {"query" : category.getPath(),
                                 "depth" : 1},
                         sort_on = "getObjPositionInParent")

        for category in brains:

            show_subtree = self._showSubTree(category)
            
            # At the moment we using the criterion of show_subtree to decide 
            # whether the category is current selected or not. This results 
            # in current_item for all parent categories of the current selected
            # category.
            if show_subtree == True:
                klass = "navTreeCurrentItem visualIconPadding"
            else:
                klass = "visualIconPadding"

            if show_subtree == True:
                sub_categories = self._getSubCategories(category)
            else:
                sub_categories = []
                                    
            result.append({
                "klass"              : klass,
                "url"                : category.getURL,
                "description"        : category.Description,
                "title"              : category.Title,
                "amount_of_products" : category.total_amount_of_products,
                "subcategories"      : sub_categories,
                "show_subtree"       : show_subtree,
            })

        return result 
    
    # This is not used at the moment as we use the show_subtree criterion to 
    # mark current categories. This method can be used to just select the
    # current category without its parents. However the current approach should 
    # be faster, too.
    def _getItemClass(self, category):
        """Returns the css class of the category, which differs between current
        or not current.
        """
        context_url  = self.context.absolute_url()
        category_url = category.getURL()
    
        if context_url == category_url:
            return "navTreeCurrentItem visualIconPadding"
        elif self.context.portal_type == "Product":
            try:
                product_category = \
                self.context.getBRefs("category_products")[0]
            except IndexError:
                return "visualIconPadding"
        
            # UID doesn't work here. Don't know why yet.
            if category.getPath() == "/".join(product_category.getPhysicalPath()):
                return "navTreeCurrentItem visualIconPadding"     
            
        return "visualIconPadding"

    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()
        
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