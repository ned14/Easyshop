# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq
from Products.AdvancedQuery import In

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShopManagement

class ProductRelationsView(BrowserView):
    """
    """
    def getCategories(self):
        """
        """
        if self.request.get("sent", None) is None:
            return None
        
        searchtext = self.request.get("searchtext")
        
        assigend_categories = []
        cm = ICategoryManagement(self.context)
        for category in cm.getTopLevelCategories():
            assigend_categories.append(category.UID())
                        
        shop = IShopManagement(self.context).getShop()
        catalog = getToolByName(self.context, "portal_catalog")
        
        query = Eq("path", "/".join(shop.getPhysicalPath()))
        query = And(query, Eq("portal_type", "Category"))

        if searchtext != "":
            searchtext += "*"
            query = And(query, Eq("Title", searchtext))
            
        brains = catalog.evalAdvancedQuery(query)
                
        result = []
        for category in brains:
            
            if category.UID in assigend_categories:
                continue
                
            result.append({
                "uid"   : category.UID,
                "title" : category.Title,
            })
        
        return result

    def getAssignedCategories(self):
        """
        """
        cm = ICategoryManagement(self.context)
        
        result = []
        for category in cm.getTopLevelCategories():
            result.append({
                "uid"   : category.UID(),
                "title" : category.Title(),
            })
            
        return result
        
    def deleteCategories(self):
        """
        """
        uids = self.request.get("uid", [])
        if isinstance(uids, (list, tuple)) == False:
            uids = (uids,)

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.evalAdvancedQuery(
            In("UID", uids)
        )

        for brain in brains:
            category = brain.getObject()
            category.deleteReference(self.context, "categories_products")

        url = self.context.absolute_url() + "/relations-view"
        self.request.response.redirect(url)
                    
    def assignCategories(self):
        """
        """
        uids = self.request.get("uid", [])
        if isinstance(uids, (list, tuple)) == False:
            uids = (uids,)
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.evalAdvancedQuery(
            In("UID", uids)
        )

        for brain in brains:
            category = brain.getObject()
            category.addReference(self.context, "categories_products")
        
        url = self.context.absolute_url() + "/relations-view"
        self.request.response.redirect(url)