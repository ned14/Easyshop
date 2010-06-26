# zope imports
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ITaxManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IShopManagement

class TaxesView(BrowserView):
    """
    """
    def getDefaultTaxes(self):
        """
        """
        tm = ITaxManagement(IShopManagement(self.context).getShop())
        nc = queryUtility(INumberConverter)
        
        result = []
        for tax in tm.getDefaultTaxes(): 
            result.append({
                "id"        : tax.getId(),
                "title"     : tax.Title(),
                "rate"      : nc.floatToTaxString(tax.getRate()),
                "up_link"   : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), tax.getId()),
                "down_link" : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), tax.getId()),
                "url"       : tax.absolute_url(),
                "amount_of_criteria" : self._getAmountOfCriteria(tax.getId()),
            })
        
        return result
            
    def getCustomerTaxes(self):
        """
        """    
        tm = ITaxManagement(IShopManagement(self.context).getShop())
        nc = queryUtility(INumberConverter)
                
        result = []
        for tax in tm.getCustomerTaxes():
            result.append({
                "id"        : tax.getId(),
                "title"     : tax.Title(),
                "rate"      : nc.floatToTaxString(tax.getRate()),
                "up_link"   : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), tax.getId()),
                "down_link" : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), tax.getId()),
                "url"       : tax.absolute_url(),
                "amount_of_criteria" : self._getAmountOfCriteria(tax.getId()),
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