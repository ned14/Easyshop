# Five imports
from Products.Five.browser import BrowserView

# Zope imports
from ZTUtils import make_query

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone import Batch

# easyshop imports
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IProductManagement

class ManageProductsView(BrowserView):
    """
    """
    def getProducts(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pm = IProductManagement(shop)
        
        result = []
        for product in pm.getProducts():
            result.append({
                "uid"   : product.UID,
                "title" : product.Title,                
            })
        
        # Get start page                             
        b_start  = self.request.get('b_start', 0);

        batch = Batch(result, 20, int(b_start), orphan=0)
        
        # Calculate Batch
        return {
            "batch"        : batch,
            "next_url"     : self._getNextUrl(batch),
            "previous_url" : self._getPreviousUrl(batch)
        }
        
        
    def _getNextUrl(self, batch):
        """
        """
        try:
            start_str = batch.next.first
        except AttributeError:
            start_str = None 
            
        query = make_query(self.request.form, {batch.b_start_str:start_str})
        return "%s/manage-products?%s" % (self.context.absolute_url(), query)

    def _getPreviousUrl(self, batch):
        """
        """
        try:
            start_str = batch.previous.first
        except AttributeError:
            start_str = None 
            
        query = make_query(self.request.form, {batch.b_start_str:start_str})
        return "%s/manage-products?%s" % (self.context.absolute_url(), query)
        
        
    def addProducts(self):
        """
        """
        product_uids = self.request.get("product_uids", [])

        self.context.setProducts(product_uids)
        self.context.reindexObject()
        
        self.request.response.redirect("manage-products")