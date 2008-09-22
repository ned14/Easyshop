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
            content.append("<a href='%s'>%s</a>" % (product.absolute_url(), product.absolute_url()))
            rm = IRatingManager(product)        
            ratings = rm.getAllRatings()
            
            for rating in ratings:
                
                if rating.name is not None:
                    rating.name = rating.name.replace("&Atilde;&curren;", u'\xe4')
                    rating.name = rating.name.replace("&Atilde;&frac14;", u'\xfc')
                    rating.name = rating.name.replace("&Atilde;&para;", u'\xf6')
                    
                if rating.comment is not None:
                    
                    rating.comment = rating.comment.replace("&Atilde;&curren;", u'\xe4')
                    rating.comment = rating.comment.replace("&Atilde;&frac14;", u'\xfc')
                    rating.comment = rating.comment.replace("&Atilde;&para;", u'\xf6')
                                        
                if rating.subject is not None:
                    rating.subject = rating.subject.replace("&Atilde;&curren;", u'\xe4')
                    rating.subject = rating.subject.replace("&Atilde;&frac14;", u'\xfc')
                    rating.subject = rating.subject.replace("&Atilde;&para;", u'\xf6')
        
        result = "<html>"        
        result += "<br/>".join(content)
        result += "</html>"
        
        return result 
