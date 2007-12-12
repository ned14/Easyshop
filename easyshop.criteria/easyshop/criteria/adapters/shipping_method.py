# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IShippingMethodCriteria
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity


class ShippingMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IShippingMethodCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the selected shipping method of the current customer
        is within selected shipping methods of this criterion.
        """        
        shop = IShopManagement(self.context).getShop()
        sm = IShippingMethodManagement(shop)
        selected_method = sm.getSelectedShippingMethod()
                
        if selected_method is not None and \
           selected_method.getId() in self.context.getShippingMethods():
            return True
        else:
            return False