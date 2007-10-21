# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IShopManagement

class IPaymentMethodsView(Interface):    
    """
    """
    def getPaymentMethods():
        """Returns the payment prices of the shop.
        """
    
class PaymentMethodsView(BrowserView):
    """
    """
    implements(IPaymentMethodsView)

    def getPaymentMethods(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pm = IPaymentManagement(shop)
                
        result = []
        for payment_method in pm.getPaymentMethods():            
            result.append({
            
                "id"       : payment_method.getId(),            
                "title"    : payment_method.Title(),
                "url"      : payment_method.absolute_url(),
                "up_url"   : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), payment_method.getId()),
                "down_url" : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), payment_method.getId()),
                "amount_of_criteria" : self._getAmountOfCriteria(payment_method.getId())
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
    