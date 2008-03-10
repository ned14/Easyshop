# Python imports
import re

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from easyshop.core.interfaces import IShopManagement

class SearchView(BrowserView):
    """
    """    
    def getSearchResults(self):
        """
        """
        searchable_text = self.request.get("SearchableText", "")
        if searchable_text == "":
            return []
        
        if re.match("^\w+$", searchable_text) is not None:
            searchable_text = "%" + searchable_text
            
        shop    = IShopManagement(self.context).getShop()
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(shop.getPhysicalPath()),
            portal_type = "Product",
            SearchableText = searchable_text,
        )
    
        return brains