# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import INumberConverter

class ITaxView(Interface):    
    """
    """
    def getCriteria():
        """Returns all criteria.
        """
    
    def getRate():
        """Returns the rate of the tax.
        """   

class TaxView(BrowserView):
    """
    """
    implements(ITaxView)
    
    def getCriteria(self):
        """
        """
        result = []
        for index, criteria in enumerate(self.context.objectValues()):

            if index % 2 == 0:
                klass = "odd"
            else:
                klass = "even"
                
            result.append({
                "title"  : criteria.Title(),
                "url"    : criteria.absolute_url(),
                "value"  : criteria.getValue(),
                "class"  : klass,                  
            })
        
        return result
        
    def getRate(self):
        """
        """
        nc = queryUtility(INumberConverter)
        return nc.floatToTaxString(self.context.getRate())
