# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IWidthCriteria
from easyshop.core.interfaces import IShopManagement

class WidthCriteriaValidity:
    """Adapter which provides IValidity for width criteria content objects.
    """
    implements(IValidity)
    adapts(IWidthCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True, if the total width of the cart is greater than the
        entered criteria width.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()
        
        # max width
        cart_width = 0
        if cart is not None:
            for item in IItemManagement(cart).getItems():
                if item.getProduct().getWidth() > cart_width:
                    cart_width = item.getProduct().getWidth()
            
        if self.context.getOperator() == ">=":
            if cart_width >= self.context.getWidth():
                return True
        else:
            if cart_width < self.context.getWidth():
                return True

        return False
