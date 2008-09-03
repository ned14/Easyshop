# zope imports
from zope.component import getUtility

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from iqpp.easyshop.interfaces import INumberConverter
from iqpp.easyshop.interfaces import ICurrencyManagement
from iqpp.easyshop.interfaces import IShopManagement

class DiscountView(BrowserView):
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
        
    def getValue(self):
        """
        """
        if self.context.getType() == "absolute":
            cm = ICurrencyManagement(IShopManagement(self.context).getShop())
            return cm.priceToString(self.context.getValue())
        else:
            c = getUtility(INumberConverter)
            return c.floatToTaxString(self.context.getValue())