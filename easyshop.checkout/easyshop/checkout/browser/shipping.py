# Zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IShippingManagement

class ICheckOutShippingView(Interface):    
    """Provides methods for the selection of shipping methods within the
    checkout process.
    """    
    
    def getShippingMethods():
        """
        """
        
class CheckOutShippingView(BrowserView):
    """
    """
    implements(ICheckOutShippingView)
    
    def getShippingMethods(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        selected_shipping_id = customer.getSelectedShippingMethod()
        
        sm = IShippingManagement(self.context)
        
        shipping_methods = []
        for shipping in sm.getShippingMethods():

            if selected_shipping_id == shipping.getId():
                checked = True
            else:
                checked = False
                            
            shipping_methods.append({
                "id" : shipping.getId(),
                "title" : shipping.Title,
                "description" : shipping.Description,
                "checked" : checked,
            })
            
        return shipping_methods