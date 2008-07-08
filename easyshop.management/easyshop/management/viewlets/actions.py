# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement

class ActionsViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('actions.pt')

    def getSelectedCategories(self):
        """
        """
        selected_categories = self.request.get("search_category", [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (selected_categories,)
        
        return selected_categories
    
    def getSelectedProducts(self):
        """
        """
        selected_uids = self.request.get("selected_uids")
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = selected_uids
        )
        
        result = []
        for brain in brains:
            product = brain.getObject()
            
            cm = ICategoryManagement(product)
            categories = cm.getTopLevelCategories()

            categories = ", ".join([c.Title() for c in categories])
            
            result.append({
                "uid"   : product.UID(),
                "id"    : product.getId(),
                "title" : product.Title(),
                "price" : product.getPrice(),
                "categories" : categories,
            })
            
        return result
        
    def showChangePrice(self):
        """
        """
        return self.request.get("action") == "change_price"
        
    def showRename(self):
        """
        """
        return self.request.get("action") == "rename"
        
    def showAddToGroup(self):
        """
        """
        return self.request.get("action") == "add_to_group"

    def showChangeCategory(self):
        """
        """
        return self.request.get("action") in ("change_category")