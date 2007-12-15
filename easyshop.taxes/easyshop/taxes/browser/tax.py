# zope imports
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import INumberConverter

class TaxView(BrowserView):
    """
    """
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
