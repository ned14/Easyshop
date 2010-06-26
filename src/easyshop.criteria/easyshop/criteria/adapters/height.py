# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IHeightCriteria
from easyshop.core.interfaces import IShopManagement

class HeightCriteriaValidity:
    """Adapter which provides IValidity for height criteria content objects.
    """
    implements(IValidity)
    adapts(IHeightCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True, if the total height of the cart is greater than the
        entered criteria height.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()

        # total height
        cart_height = 0
        if cart is not None:
            for item in IItemManagement(cart).getItems():
                cart_height += (item.getProduct().getHeight() * item.getAmount())
            
        if self.context.getOperator() == ">=":
            if cart_height >= self.context.getHeight():
                return True
        else:
            if cart_height < self.context.getHeight():
                return True
        return False        
