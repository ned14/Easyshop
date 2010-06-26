# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class CartsView(BrowserView):
    """
    """
    def getCarts(self):
        """
        """
        sort_on    = self.request.get("sort_on", "modified")
        sort_order = self.request.get("sort_order", "descending")

        shop = IShopManagement(self.context).getShop()
        cm = ICartManagement(shop)

        ttool = getToolByName(self.context, 'translation_service')
                
        result = []
        
        for cart in cm.getCarts():

            cart_object = cart.getObject()
            
            # items
            im = IItemManagement(cart_object)
            items = im.getItems()
            amount_of_items = len(items)
            
            if len(items) > 0:
                last_item = items[-1]
                modified = last_item.modified()
            else:
                modified = cart.modified
             
            # price
            price_float = IPrices(cart_object).getPriceGross()
            price = ICurrencyManagement(shop).priceToString(price_float)
                        
            # created
            created = ttool.ulocalized_time(cart.created, long_format=True)
            modified = ttool.ulocalized_time(modified, long_format=True)
            
            result.append({
                "id"              : cart.getId,
                "url"             : cart.getURL(),
                "created"         : created,
                "modified"        : modified,
                "amount_of_items" : amount_of_items,
                "price_float"     : price_float,             # for sorting reasons
                "price"           : price,
            })

        # There is no index for price, amount_of_items, modified (the
        # modification date of the cart is dependend on the items,
        # so default modification date is not working). So we have 
        # to order the result in another way
        
        # Yes. there is a index for id and created, but to differ makes the 
        # code more complicate than it gains speed, imo. In addition that this
        # is (just) a admin view.
        
        if sort_order == "descending":
            result.sort(lambda a, b: cmp(b[sort_on], a[sort_on]))
        else:
            result.sort(lambda a, b: cmp(a[sort_on], b[sort_on]))                
                
        return result        