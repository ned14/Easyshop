# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICombinedLengthAndGirthCriteria
from easyshop.core.interfaces import IShopManagement

class CombinedLengthAndGirthCriteriaValidity:
    """Adapter which provides IValidity for width criteria content objects.
    """
    implements(IValidity)
    adapts(ICombinedLengthAndGirthCriteria)

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
        
        max_length = 0
        max_width = 0
        total_height = 0
        
        if cart is not None:
            for item in IItemManagement(cart).getItems():
                if max_length < item.getProduct().getLength():
                    max_length = item.getProduct().getLength()
                
                if max_width < item.getProduct().getWidth():
                    max_width = item.getProduct().getWidth()
                    
                total_height += (item.getProduct().getHeight() * item.getAmount())
        
        # Calc cart girth        
        cart_girth = (2 * max_width) +  (2 * total_height) + max_length
        
        if self.context.getOperator() == ">=":
            if cart_girth >= self.context.getCombinedLengthAndGirth():
                return True
        else:
            if cart_girth < self.context.getCombinedLengthAndGirth():
                return True

        return False        
