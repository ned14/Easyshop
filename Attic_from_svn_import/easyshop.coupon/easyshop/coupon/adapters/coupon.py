# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.coupon.interfaces import ICoupon
from easyshop.coupon.interfaces import ICouponManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement


class CouponValidity:
    """Adapter which provides IValidity for coupon content objects.
    """
    implements(IValidity)
    adapts(ICoupon)

    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns True if the entered coupon code is valid
        """
        shop = IShopManagement(self.context).getShop()
        cm = ICouponManagement(shop)

        if cm.getValidCoupon(self.context):
            return True
        else:
            return False
