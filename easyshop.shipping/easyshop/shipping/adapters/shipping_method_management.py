# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from iqpp.easyshop.interfaces import ICustomerManagement
from iqpp.easyshop.interfaces import IShippingMethodManagement
from iqpp.easyshop.interfaces import IShop
from iqpp.easyshop.interfaces import IShopManagement
from iqpp.easyshop.interfaces import IValidity

class ShippingMethodManagement(object):
    """An adapter which provides IShippingMethodManagement for shop content 
    objects.
    """    
    implements(IShippingMethodManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.shipping_methods = self.context.shippingmethods
        
    def getSelectedShippingMethod(self):
        """
        """
        cm = ICustomerManagement(IShopManagement(self.context).getShop())
        customer = cm.getAuthenticatedCustomer()        
        shipping_method_id = customer.selected_shipping_method
        
        return self.getShippingMethod(shipping_method_id)
        
    def getShippingMethod(self, id):
        """
        """
        try:
            return self.shipping_methods[id]
        except KeyError:
            return None    

    def getShippingMethods(self, check_validity=False):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        shipping_methods = []
        for shipping_method in self.shipping_methods.objectValues():

            if check_validity and \
               IValidity(shipping_method).isValid() == False:
                continue
            
            if mtool.checkPermission("View", shipping_method) is not None:
                shipping_methods.append(shipping_method)
        
        return shipping_methods
