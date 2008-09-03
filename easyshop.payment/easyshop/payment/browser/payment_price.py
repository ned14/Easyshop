# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from iqpp.easyshop.interfaces import ICurrencyManagement
from iqpp.easyshop.interfaces import IShopManagement

class PaymentPriceView(BrowserView):
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
        
    def getPrice(self):
        """
        """        
        cm = ICurrencyManagement(IShopManagement(self.context).getShop())
        return cm.priceToString(self.context.getPrice())
