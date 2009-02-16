# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class CacheView(BrowserView):
    """
    """ 
    def reset_cache(self):
        """
        """
        # CMFCore imports
        catalog = getToolByName(self.context, "portal_catalog")
        for brain in catalog.searchResults(portal_type = ["ProductVariant"]):
            product = brain.getObject()
            if hasattr(product, "cache"):
               product.cache.clear()