# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity

class CartDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart content objects.
    """
    implements(IDiscountsCalculation)
    adapts(ICart)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def getDiscount(self):
        """Returns calculated discounts.
        """
        return self.getDiscountsInformation()["discounts"]
        
class CartItemDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart item content
    objects.
    """
    implements(IDiscountsCalculation)
    adapts(ICartItem)

    def __init__(self, context):
        """
        """
        self.context = context

    def getDiscount(self):
        """Returns the first valid discount or None.
        """
        shop = IShopManagement(self.context).getShop()
        for discount in IDiscountsManagement(shop).getDiscounts():
            if IValidity(discount).isValid(self.context) == True:
                return discount
        
        return None