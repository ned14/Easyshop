import transaction

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IPrices

class MigrateView(BrowserView):
    """
    """
    # def migrate(self):
    #     """
    #     """
    #     catalog = getToolByName(self.context, "portal_catalog")
    #     brains = catalog.searchResults(
    #         portal_type = "ProductVariant",
    #     )
    #     
    #     result = ""
    #     for brain in brains:
    #         product = brain.getObject()
    #         
    #         if product.getForSale():
    #             price_1 = product.getSalePrice()            
    #         else:
    #             price_1 = product.getPrice()            
    #         price_2 = IPrices(product).getPriceGross()
    #         
    #         if price_1 != price_2:
    #             result += "%s %s %s\n" % (product.Title(), price_1, price_2)
    #         
    #     return result

    def migrate(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Product",
        )
        
        result = ""
        for brain in brains:
            product = brain.getObject()
            
            if hasattr(product, "cache"):
                product.cache.clear()