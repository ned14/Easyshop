import re

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
        for uid_with_quantity in self.context.getAccessories():
            uid, quantity = uid_with_quantity.split(":")
            brain = catalog.searchResults(UID = uid)[0]
            result.append({
                "uid"   : uid,
                "title" : brain.Title,
                "quantity": quantity,
            })
            
        return result
            
    def getProducts(self):
        """
        """
        accessories_uids = [a["uid"] for a in self.getAccessories()]
        
        product_title = self.request.get("product-title", "")
        if product_title == "":
            return []
            
        catalog = getToolByName(self.context, "portal_catalog")                

        query = Eq("portal_type", "Product") & Eq("Title", product_title)
        brains = catalog.evalAdvancedQuery(query)
        
        result = []
        for brain in brains:
            if brain.UID not in accessories_uids:
                result.append({
                    "title" : brain.Title,
                    "uid"   : brain.UID
                })

        return result

    def addAccessories(self):
        """
        """
        # Collect new products
        new_uids = self.request.form.get("new-products", [])
        new_uids = utils.tuplize(new_uids)
        
        # Add quantities to new products
        new_uids_with_quantities = []
        for new_uid in new_uids:
            quantity = self.request.get("%s_quantity" % new_uid, 1)
            new_uids_with_quantities.append("%s:%s" % (new_uid, quantity))
            
        existing_uids = self.context.getAccessories()
        
        unique_uids = self.unify(existing_uids, new_uids_with_quantities)
        self.context.setAccessories(unique_uids)

        self.redirect()
        
    def updateAccessories(self):
        """
        """
        uids = self.request.get("accessories", [])
        uids = utils.tuplize(uids)
        
        uids_with_quantities = []
        for new_uid in uids:
            quantity = self.request.get("%s_quantity" % new_uid, 1)
            uids_with_quantities.append("%s:%s" % (new_uid, quantity))
        
        self.context.setAccessories(uids_with_quantities)
        self.redirect()
        
    def unify(self, old_uids_with_quantities, new_uids_with_quantities):
        """
        """
        result = list(old_uids_with_quantities)
        
        # collect old uids without quantities        
        old_uids = []
        for old_uid in old_uids_with_quantities:
            uid, quantity = old_uid.split(":")
            old_uids.append(uid)
                        
        for new_uid in new_uids_with_quantities:
            uid, quantity = new_uid.split(":")
            if uid not in old_uids:       # compare uids without quantity
                result.append(new_uid)    # add uid with quantity here
        return result
        
    def redirect(self, url="manage-accessories-view"):
        """
        """
        url = "%s/%s" % (self.context.absolute_url(), url)
        self.request.response.redirect(url)