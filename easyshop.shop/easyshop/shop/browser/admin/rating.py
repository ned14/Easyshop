# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# rating imports
from iqpp.plone.rating.adapters.manager import IRatingManager

# AdvancedQuery
from Products.AdvancedQuery import And
from Products.AdvancedQuery import Eq
from Products.AdvancedQuery import Ge

class RatingView(BrowserView):
    """
    """
    def cleanupRatings(self):
        content = []
        
        catalog = getToolByName(self.context, "portal_catalog")
        
        query = Eq("portal_type", "Product") & Ge("amount_of_ratings", 1)
        brains = catalog.evalAdvancedQuery(query)
    
        for brain in brains:
            product = brain.getObject()
            
            rm = IRatingManager(product)        
            ratings = rm.getAllRatings()
            
            for rating in ratings:
                if rating.comment is not None:                     
                    content.append(rating.comment)
                if rating.subject is not None:
                    content.append(rating.subject)
                
        return "<br/>".join(content)
