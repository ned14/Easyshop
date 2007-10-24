# Five imports
from Products.Five.browser import BrowserView

# Easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

class CustomersContainerView(BrowserView):
    """
    """
    def getCustomers(self):
        """
        """
        shop = IShopManagement(self.context).getShop()                        
        cm = ICustomerManagement(shop)
        
        result = []
        for customer in cm.getCustomers():
            result.append({
                "id" : customer.getId(),
                # "fullname" : customer.getFullname(),
                # "email" : customer.getEmail(),
                "url" : customer.absolute_url(),
            })
            
        return result