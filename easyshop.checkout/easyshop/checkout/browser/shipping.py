# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingManagement

class ShippingSelectForm(BrowserView):
    """
    """    
    def getShippingMethods(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_shipping_id = customer.selectedShippingMethod
        
        sm = IShippingManagement(self.context)
        
        shipping_methods = []
        for shipping in sm.getShippingMethods():

            if selected_shipping_id == shipping.getId():
                checked = True
            elif selected_shipping_id == "" and shipping.getId() == "default":
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
        
    def selectShippingMethod(self):
        """
        """
        # Set the selected shipping mehtod
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()        
        customer.selectedShippingMethod = self.request.get("id")

        # Go to next url
        cm = ICheckoutManagement(self.context)
        cm.redirectToNextURL("SELECTED_SHIPPING_METHOD")