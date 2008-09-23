# Five imports
from Products.Five.browser import BrowserView

# CMFPlone imports
from Products.CMFPlone import utils

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import Eq

class ManageAccessoriesView(BrowserView):
    """
    """
    def getAccessories(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        
        result = []
        for uid in self.context.getAccessories():
            brain = catalog.searchResults(UID = uid)[0]
            result.append({
                "uid"   : uid,
                "title" : brain.Title
            })
            
        return result
            
    def getProducts(self):
        """
        """
        product_title = self.request.get("product-title", "")
        if product_title == "":
            return []
            
        catalog = getToolByName(self.context, "portal_catalog")                

        query = Eq("portal_type", "Product") & Eq("Title", product_title)
        brains = catalog.evalAdvancedQuery(query)
        
        result = []
        for brain in brains: 
            result.append({
                "title" : brain.Title,
                "uid"   : brain.UID
            })

        return result

    def addAccessories(self):
        """
        """
        new_uids = self.request.get("new-products", [])
        new_uids = utils.tuplize(new_uids)
        
        existing_uids = self.context.getAccessories()
        
        unique_uids = self.unify(existing_uids, new_uids)
        self.context.setAccessories(unique_uids)

        self.redirect()
        
    def updateAccessories(self):
        """
        """
        uids = self.request.get("accessories", [])
        uids = utils.tuplize(uids)
        
        self.context.setAccessories(uids)
        
        self.redirect()
        
    def unify(self, old, new):
        """
        """
        result = list(old)
        
        for new_uid in new:
            if new_uid not in old:
                result.append(new_uid)
        return result
        
    def redirect(self, url="manage-accessories-view"):
        """
        """
        url = "%s/%s" % (self.context.absolute_url(), url)
        self.request.response.redirect(url)