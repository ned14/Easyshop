# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class StockRulesContainerView(BrowserView):
    """
    """
    def getStockRules(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm   = IStockManagement(shop)
                
        result = []
        for stock_rule in sm.getStockRules():
            
            information = IData(stock_rule).asDict()
            
            result.append({
                "id"          : stock_rule.getId(),
                "title"       : stock_rule.Title(),
                "description" : stock_rule.Description(),
                "available"   : information["available"],
                "time_period" : information["time_period"],
                "url"         : stock_rule.absolute_url(),
                "up_url"      : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), stock_rule.getId()),
                "down_url"    : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), stock_rule.getId()),
                "amount_of_criteria" : len(stock_rule.objectIds()),
            })

        return result