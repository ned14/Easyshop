# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

class IShippingMethodView(Interface):    
    """
    """
    def getCriteria():
        """Returns all criteria.
        """
    
class ShippingMethodView(BrowserView):
    """
    """
    implements(IShippingMethodView)
    
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