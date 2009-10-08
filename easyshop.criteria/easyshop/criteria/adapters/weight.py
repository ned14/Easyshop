# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IWeightCriteria
from easyshop.core.interfaces import IShopManagement

class WeightCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content objects.
    """
    implements(IValidity)
    adapts(IWeightCriteria)

    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns True, if the total weight of the cart is greater than the
        entered criteria weight.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()

        # total weight
        if cart is not None:
            cart_weight = 0
            for item in IItemManagement(cart).getItems():
                cart_weight += (item.getProduct().getWeight() * item.getAmount())

            if self.context.getOperator() == ">=":
                if cart_weight >= self.context.getWeight():
                    return True
            else:
                if cart_weight < self.context.getWeight():
                    return True

        return False
