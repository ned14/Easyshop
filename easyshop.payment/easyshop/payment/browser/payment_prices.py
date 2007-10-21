# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IPaymentPrices
from Products.EasyShop.interfaces import IShopManagement

class PaymentPricesView(BrowserView):
    """
    """
    def getPaymentPrices(self):
        """
        """
        shop = IShopManagement(self.context).getShop()        
        pp = IPaymentPrices(shop)
        cm = ICurrencyManagement(shop)
                
        result = []
        for payment_price in pp.getPaymentPrices():
            
            price = cm.priceToString(payment_price.getPriceGross())
            
            result.append({
                "id"       : payment_price.getId(),            
                "title"    : payment_price.Title(),
                "price"    : price,
                "url"      : payment_price.absolute_url(),
                "up_url"   : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), payment_price.getId()),
                "down_url" : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), payment_price.getId()),
                "amount_of_criteria" : self._getAmountOfCriteria(payment_price.getId())
            })

        return result
        
    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            tax = self.context[id]
        except IndexError:
            return 0
            
        return len(tax.objectIds())