# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IShopManagement

class DiscountsContainerView(BrowserView):
    """
    """
    def getDiscounts(self):
        """
        """
        shop = IShopManagement(self.context).getShop()        
        dm   = IDiscountsManagement(shop)
        cm   = ICurrencyManagement(shop)
                
        result = []
        for discount in dm.getDiscounts():
            
            value = cm.priceToString(discount.getValue())
            
            result.append({
                "id"          : discount.getId(),            
                "title"       : discount.Title(),
                "description" : discount.Description(),
                "value"       : value,
                "url"         : discount.absolute_url(),
                "up_url"      : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), discount.getId()),
                "down_url"    : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), discount.getId()),
                "amount_of_criteria" : self._getAmountOfCriteria(discount.getId())
            })

        return result
        
    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            tax = self.context[id]
        except KeyError:
            return 0
            
        return len(tax.objectIds())