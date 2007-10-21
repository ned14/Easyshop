# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import IShippingManagement
from Products.EasyShop.interfaces import IShopManagement

class ShippingMethodsView(BrowserView):
    """
    """
    def getShippingMethods(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pm = IShippingManagement(shop)
                
        result = []
        for shipping_method in pm.getShippingMethods():
            result.append({
            
                "id"       : shipping_method.getId(),            
                "title"    : shipping_method.Title(),
                "url"      : shipping_method.absolute_url(),
                "up_url"   : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), shipping_method.getId()),
                "down_url" : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), shipping_method.getId()),
                "amount_of_criteria" : self._getAmountOfCriteria(shipping_method.getId())
            })

        return result
        
    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            method = self.context[id]
        except IndexError:
            return 0
            
        return len(method.objectIds())
