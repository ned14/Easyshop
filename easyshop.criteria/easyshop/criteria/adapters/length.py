# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ILengthCriteria
from easyshop.core.interfaces import IShopManagement

class LengthCriteriaValidity:
    """Adapter which provides IValidity for length criteria content objects.
    """
    implements(IValidity)
    adapts(ILengthCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True, if the total length of the cart is greater than the
        entered criteria length.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()
        
        # max_length
        cart_length = 0
        if cart is not None:
            for item in IItemManagement(cart).getItems():
                if item.getProduct().getLength() > cart_length:
                    cart_length = item.getProduct().getLength()
        
        if self.context.getOperator() == ">=":
            if cart_length >= self.context.getLength():
                return True
        else:
            if cart_length < self.context.getLength():
                return True
            
        return False        
