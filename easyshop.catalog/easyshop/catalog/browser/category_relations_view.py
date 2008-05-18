# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq
from Products.AdvancedQuery import In

# easyshop imports
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class CategoryRelationsView(BrowserView):
    """
    """
    def getProducts(self):
        """
        """
        if self.request.get("sent", None) is None:
            return None
        
        searchtext = self.request.get("searchtext")
        
        assigned_products = []
        pm = IProductManagement(self.context)
        for product in pm.getProducts():
            assigned_products.append(product.UID())
                        
        shop = IShopManagement(self.context).getShop()
        catalog = getToolByName(self.context, "portal_catalog")
        
        query = Eq("path", "/".join(shop.getPhysicalPath()))
        query = And(query, Eq("portal_type", "Product"))

        if searchtext != "":
            searchtext += "*"
            query = And(query, Eq("Title", searchtext))
            
        brains = catalog.evalAdvancedQuery(query)
                
        result = []
        for product in brains:
            
            if product.UID in assigned_products:
                continue
                
            result.append({
                "uid"   : product.UID,
                "title" : product.Title,
            })
        
        return result

    def getAssignedProducts(self):
        """
        """
        pm = IProductManagement(self.context)
        
        result = []
        for product in pm.getProducts():
            result.append({
                "uid"   : product.UID(),
                "title" : product.Title(),
            })
            
        return result
        
    def deleteProducts(self):
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
            product = brain.getObject()
            self.context.deleteReference(product, "categories_products")

        url = self.context.absolute_url() + "/relations-view"
        self.request.response.redirect(url)
                    
    def assignProducts(self):
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
            product = brain.getObject()
            self.context.addReference(product, "categories_products")
        
        url = self.context.absolute_url() + "/relations-view"
        self.request.response.redirect(url)