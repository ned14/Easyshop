# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IShippingMethodCriteria
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class ShippingMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content
    objects.
    """
    implements(IValidity)
    adapts(IShippingMethodCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether the selected shipping method of the current customer
        is within selected shipping methods of this criterion.
        """        
        shop = IShopManagement(self.context).getShop()
        sm = IShippingManagement(shop)
        selected_method = sm.getSelectedShippingMethod()
                
        if selected_method.getId() in self.context.getShippingMethods():
            return True
        else:
            return False