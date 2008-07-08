# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq
from Products.AdvancedQuery import In

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement

class SelectProductsViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('select_products.pt')
    
    def getProducts(self):
        """
        """
        if self.request.get("form-sent") is None:
            return []
            
        query =  Eq("path", "/".join(self.context.getPhysicalPath()))
        query &= Eq("object_provides", "easyshop.core.interfaces.catalog.IProduct")
        
        search_text = self.request.get("search_text", "")
        search_category = self.request.get("search_category", [])
        
        if search_text != "":
            query &= Eq("Title", search_text)
        
        if len(search_category) > 0:
            query &= In("categories", search_category)

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.evalAdvancedQuery(query)
        
        result = []
        for brain in brains:
            product = brain.getObject()
            
            categories = ", ".join([c.Title() for c in product.getCategories()])
            
            result.append({
                "uid"   : product.UID(),
                "title" : product.Title(),
                "price" : product.getPrice(),
                "categories" : categories
            })

        return result
        
    def getSelectedCategories(self):
        """
        """
        selected_categories = self.request.get("search_category", [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (selected_categories,)
        
        return selected_categories