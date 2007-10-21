# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IShopManagement

class IPaymentPriceView(Interface):    
    """
    """
    def getCriteria():
        """Returns all criteria.
        """
    
    def getPrice():
        """Returns the price gross of the payment price object.
        """   

class PaymentPriceView(BrowserView):
    """
    """
    implements(IPaymentPriceView)
    
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
        return cm.priceToString(self.context.getPriceGross())
