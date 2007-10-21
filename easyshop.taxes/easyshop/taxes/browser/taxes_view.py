# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ITaxManagement
from Products.EasyShop.interfaces import INumberConverter

class ITaxesView(Interface):    
    """
    """
    def getDefaultTaxes():
        """Returns the default taxes for the country.
        """    

    def getCustomerTaxes():
        """Returns special taxes for the customers.
        """
        
class TaxesView(BrowserView):
    """
    """
    implements(ITaxesView)

    def getDefaultTaxes(self):
        """
        """
        tm = ITaxManagement(self.context.getShop())
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
        tm = ITaxManagement(self.context.getShop())
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
        except IndexError:
            return 0
            
        return len(tax.objectIds())
    