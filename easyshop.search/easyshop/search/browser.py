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
        
        shop = IShopManagement(self.context).getShop()
        catalog = getToolByName(self.context, "portal_catalog")

        results_glob = catalog.searchResults(
            path = "/".join(shop.getPhysicalPath()),
            portal_type = "Product",
            SearchableText = searchable_text,
        )

        searchable_text = searchable_text.replace("*", "")
        results_similar = catalog.searchResults(
            path = "/".join(shop.getPhysicalPath()),
            portal_type = "Product",
            SearchableText = "%" + searchable_text,
        )

        unique = {}
        for result in results_glob:
            unique[result.UID] = result

        for result in results_similar:
            unique[result.UID] = result
    
        return unique.values()