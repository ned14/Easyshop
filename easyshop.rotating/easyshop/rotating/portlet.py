# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IShopManagement

# iqpp.plone.rotating imports
from iqpp.plone.rotating.interfaces import IRotating
from iqpp.plone.rotating.portlets.rotating import Renderer as RotatingRenderer

class Renderer(RotatingRenderer):
    
    render = ViewPageTemplateFile('portlet.pt')    

    def getRotatingObjects(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        cm = ICurrencyManagement(shop)
        
        catalog = getToolByName(self.context, "portal_catalog")
        
        path = self.data.path.encode("utf-8")
        obj = self.context.restrictedTraverse(path)
        
        result = []
        for item in IRotating(obj).getItems(self.data.limit):

            brains = catalog.searchResults(UID = item["uid"])
            product = brains[0].getObject()
            
            standard_price = IPrices(product).getPriceForCustomer(effective=False)
            price = IPrices(product).getPriceForCustomer()
                
            item["for_sale"] = product.getForSale()
            item["standard_price"] = cm.priceToString(standard_price)
            item["price"] = cm.priceToString(price)
            
            result.append(item)
            
        return result
