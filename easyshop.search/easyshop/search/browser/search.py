# plone imports
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq

class SearchView(BrowserView):
    """Provides miscellanous methods for searching.
    """

    @memoize
    def getSearchResults(self, simple=True, searchable_text=None):
        """
        """
        if searchable_text is None:
            searchable_text = self.request.get("SearchableText", "")
                
        if searchable_text == "":
            return []
        
        utool = getToolByName(self.context, "portal_url")
        portal_url = "/".join(utool.getPortalObject().getPhysicalPath())
        
        properties = getToolByName(self.context, "portal_properties").site_properties
        shop_path = portal_url + properties.easyshop_path
                
        catalog = getToolByName(self.context, "portal_catalog")

        # Store for later use
        searchable_text_orig = searchable_text
        
        # Glob Search
        if searchable_text.find("*") == -1:
            searchable_text = " ".join(["*%s*" % x for x in searchable_text.split()])

        query = And(Eq("path", shop_path), 
                    Eq("portal_type", "Product"),
                    Eq("Title", searchable_text))

        if simple == False:
            category = self.request.get("category")
            if category is not None:
                query = query & Eq("categories", category)

        results_glob = catalog.evalAdvancedQuery(query)

        # Similarity Search
        searchable_text = searchable_text_orig
        searchable_text = searchable_text.replace("*", "")
        searchable_text = searchable_text.replace("%", "")
        
        searchable_text = "%" + searchable_text
        query = And(Eq("path", shop_path), 
                    Eq("portal_type", "Product"),
                    Eq("Title", searchable_text))

        if simple == False:
            category = self.request.get("category")
            if category is not None:
                query = query & Eq("categories", category)

        results_similar = catalog.evalAdvancedQuery(query)
        
        unique = {}
        for result in results_glob:
            unique[result.UID] = result

        for result in results_similar:
            unique[result.UID] = result

        result = unique.values()     
        
        # If we haven't found anything so far, we join the search terms with 
        # "or"
        if len(result) == 0:
            searchable_text = searchable_text_orig

            searchable_text = searchable_text.replace("*", "")
            searchable_text = " OR ".join(["*%s*" % x for x in searchable_text.split()])
            
            query = And(Eq("path", shop_path), 
                        Eq("portal_type", "Product"),
                        Eq("Title", searchable_text))
                        
            if simple == False:
                category = self.request.get("category")
                if category is not None:
                    query = query & Eq("categories", category)
            
            result = catalog.evalAdvancedQuery(query)

        return result

    @memoize        
    def getSearchUrl(self):
        """
        """
        properties = getToolByName(self.context, "portal_properties").site_properties
        shop_path = properties.easyshop_path

        return shop_path + "/shop-search"