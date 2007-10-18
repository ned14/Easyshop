# CMFCore imports
from Products.CMFCore.utils import getToolByName

def deleteLayout(self):
    for brain in self.portal_catalog():
       obj = brain.getObject()
       try:
           obj.manage_delProperties(["layout"])
       except:
           pass
           
def addPaymentPricesToOrders(self):
    """
    """
    catalog = getToolByName(self, "portal_catalog")
    brains = catalog.searchResults(
        portal_type = "EasyShopOrder",
    )
    
    for brain in brains:
        obj = brain.getObject()
        
        if obj.getPaymentPriceGross() is None:
            obj.setPaymentPriceGross(0.0)
    
        if obj.getPaymentPriceNet() is None:
            obj.setPaymentPriceNet(0.0)

        if obj.getPaymentTaxRate() is None:
            obj.setPaymentTaxRate(0.0)

        if obj.getPaymentTax() is None:
            obj.setPaymentTax(0.0)

    