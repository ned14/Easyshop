# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class StockInformationContainerView(BrowserView):
    """
    """
    def getStockInformations(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm   = IStockManagement(shop)
                
        result = []
        for stock_information in sm.getStockInformations():
            
            data = IData(stock_information).asDict()
            
            result.append({
                "id"          : stock_information.getId(),
                "title"       : stock_information.Title(),
                "description" : stock_information.Description(),
                "available"   : data["available"],
                "time_period" : data["time_period"],
                "url"         : stock_information.absolute_url(),
                "up_url"      : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), stock_information.getId()),
                "down_url"    : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), stock_information.getId()),
                "amount_of_criteria" : len(stock_information.objectIds()),
            })

        return result