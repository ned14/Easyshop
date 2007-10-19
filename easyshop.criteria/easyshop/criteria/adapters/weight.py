# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IWeightCriteria

class WeightCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content
    objects.
    """
    implements(IValidity)
    adapts(IWeightCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether the total weight of the cart is greater than the
        entered price.
        """
        shop = self.context.getShop()
        cart = ICartManagement(shop).getCart()
                
        if cart is None:
            cart_weight = 0
        else:
            cart_weight = 0
            for item in IItemManagement(cart).getItems():
                cart_weight += (item.getProduct().getWeight() * item.getAmount())
            
        if cart_weight > self.context.getWeight():
            return True
        return False        
