# zope imports
from zope import schema
from zope.formlib import form
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
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
                    sub_categories = self._getSubCategories(category)
                else:
                    sub_categories = []            

                klass = "visualIconPadding"
                                                
                if len(category.getBRefs("parent_category")) > 0:
                    klass += " hasCategories"

                if show_subtree == True:
                    klass += " navTreeCurrentItem"
                        
                result.append({
                    "klass"                : klass,
                    "url"                  : category.absolute_url(),
                    "description"          : category.Description(),
                    "title"                : category.Title(),
                    "amount_of_products"   : 1,
                    "subcategories"        : sub_categories,
                    "show_subtree"         : show_subtree,
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
        
        # Check if the passed category is ancestor of context
        if ICategory.providedBy(self.context) == True:
            obj = self.context
            while obj is not None:
                if category == obj:
                    return True
                try:
                    obj = obj.getRefs("parent_category")[0]
                except IndexError:
                    obj = None
                    

        if IProduct.providedBy(self.context) == True:
            cm = ICategoryManagement(self.context)
            try:
                product_category = cm.getTopLevelCategories()[0]
            except IndexError:
                return False
            
            while ICategory.providedBy(product_category) == True:
                if product_category.UID() == category.UID:
                    return True
                product_category = product_category.aq_inner.aq_parent
    
        return False

    def _getSubCategories(self, category):
        """
        """
        result = []
    
        cm = ICategoryManagement(category)
        categories = cm.getTopLevelCategories()
        
        for category in categories:

            show_subtree = self._showSubTree(category)
            if show_subtree == True:
                sub_categories = self._getSubCategories(category)
            else:
                sub_categories = []

            klass = "visualIconPadding"
                                            
            if len(category.getBRefs("parent_category")) > 0:
                klass += " hasCategories"

            if show_subtree == True:
                klass += " navTreeCurrentItem"
                    
            result.append({
                "klass"                : klass,
                "url"                  : category.absolute_url(),
                "description"          : category.Description(),
                "title"                : category.Title(),
                "amount_of_products"   : 1,
                "subcategories"        : sub_categories,
                "show_subtree"         : show_subtree,
            })

        return result 

    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()
        
class AddForm(base.AddForm):
    """
    """
    form_fields = form.Fields(ICategoriesPortlet)
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