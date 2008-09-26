# zope imports
from zope.component import queryUtility

# easyshop imports
from easyshop.order.browser.order_view import OrderView
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IProductVariant

class RatingMailView(OrderView):
    """
    """
    def getItems(self):
        """
        """    
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        
        items = []
        item_manager = IItemManagement(self.context)
        for item in item_manager.getItems():

            product_price_gross = cm.priceToString(item.getProductPriceGross(), suffix=None)
            tax_rate = nc.floatToTaxString(item.getTaxRate())
            tax = cm.priceToString(item.getTax(), suffix=None)
            price_gross = cm.priceToString(item.getPriceGross(), suffix=None)

            # Get url. Takes care of, if the product has been deleted in the 
            # meanwhile.
            product = item.getProduct()
            if product is None:
                url = None
            else:
                if IProductVariant.providedBy(product):
                    url = product.aq_inner.aq_parent.absolute_url()
                else:
                    url = product.absolute_url()
                    
            # Properties 
            for property in item.getProperties():
                if IProductVariant.providedBy(product) == True:
                    property["show_price"] = False
                else:
                    property["show_price"] = True
            
            temp = {
                "product_title"        : item.getProductTitle(),
                "product_quantity"     : item.getProductQuantity(),
                "product_url"          : url,
                "product_price_gross"  : product_price_gross,
                "price_gross"          : price_gross,
                "tax_rate"             : tax_rate,
                "tax"                  : tax,
                "properties"           : item.getProperties(),
                "has_discount"         : abs(item.getDiscountGross()) > 0,
                "discount_description" : item.getDiscountDescription(),
                "discount"             : cm.priceToString(item.getDiscountGross(), prefix="-", suffix=None),
            }
            
            items.append(temp)

        return items