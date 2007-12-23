# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IValidity

class CartItemDiscountsManagement:
    """An adapter which provides IDiscountsManagement for cart item content
    objects.
    """
    implements(IDiscountsManagement)
    adapts(ICartItem)

    def __init__(self, context):
        """
        """
        self.context = context
        self.discounts = self.context.discounts
        
    def getDiscounts(self):
        """Returns all valid discounts.
        """
        result = []
        for discount in self.discounts.objectValues():
            if IValidity(discount).isValid(self.context) == True:
                result.append(discount)
        return result