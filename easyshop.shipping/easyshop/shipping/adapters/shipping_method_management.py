# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

class ShippingMethodManagement:
    """An adapter which provides IShippingMethodManagement for shop content 
    objects.
    """    
    implements(IShippingMethodManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.prices  = self.context.shippingprices
        self.methods = self.context.shippingmethods
        
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
            return self.methods[id]
        except KeyError:
            return None    

    def getShippingMethods(self):
        """
        """
        # Todo: By interface
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = ("ShippingMethod",),
            path = "/".join(self.methods.getPhysicalPath()),
            sort_on = "getObjPositionInParent",
        )

        # Todo: Optimize
        return [brain.getObject() for brain in brains]