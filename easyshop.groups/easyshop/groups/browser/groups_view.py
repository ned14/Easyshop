# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement

class GroupsView(BrowserView):
    """
    """    
    def getGroup(self):
        """Returns a group by given id via request.
        """
        group_id = self.request.get("group_id")
        if group_id is None:
            return None
            
        shop = self._getShop()

        # Returns group or None
        group = IGroupManagement(shop).getGroup(group_id)        

        products = []
        for product in IProductManagement(group).getProducts():
            products.append({
                "title"  : product.Title(),
                "id"     : product.getId(),
                "url"    : product.absolute_url(),
            })
            
        return {
            "title"       : group.Title(),
            "description" : group.Description(),
            "url"         : group.absolute_url(),
            "products"    : products,
        }
        
    def getGroups(self):
        """Returns groups of the shop.
        """
        shop = self._getShop()
        
        gm = IGroupManagement(shop)
        return gm.getGroups()

    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()