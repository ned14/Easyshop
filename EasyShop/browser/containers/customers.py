# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Easyshop imports
from Products.EasyShop.interfaces import ICustomerManagement

class ICustomersView(Interface):    
    """Provides methods which can be used in context of customer folder.
    """
    def getCustomers():
        """Returns all customers of the shop
        """
       
class CustomersView(BrowserView):
    """
    """
    implements(ICustomersView)
    
    def getCustomers(self):
        """
        """
        shop = self.context.getShop()                        
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