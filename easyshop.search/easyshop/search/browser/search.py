# Python imports
import re

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from easyshop.core.interfaces import IShopManagement

class SearchView(BrowserView):
    """Provides miscellanous methods for searching.
    """
    def getSearchResults(self):
        """
        """
        searchable_text = self.request.get("SearchableText", "")
        if searchable_text == "":
            return []

        properties = getToolByName(self.context, "portal_properties").site_properties
        shop_path = properties.easyshop_path
                    
        catalog = getToolByName(self.context, "portal_catalog")

        if searchable_text.find("*") == -1:
            searchable_text += "*"
            
        results_glob = catalog.searchResults(
            path = shop_path,
            portal_type = "Product",
            SearchableText = searchable_text,
        )

        searchable_text = searchable_text.replace("*", "")
        results_similar = catalog.searchResults(
            path = shop_path,
            portal_type = "Product",
            SearchableText = "%" + searchable_text,
        )

        unique = {}
        for result in results_glob:
            unique[result.UID] = result

        for result in results_similar:
            unique[result.UID] = result
    
        return unique.values()
        
    def getSearchUrl(self):
        """
        """
        properties = getToolByName(self.context, "portal_properties").site_properties
        shop_path = properties.easyshop_path

        return shop_path + "/shop-search"