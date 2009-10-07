# -*- extra stuff goes here -*-
from coupon import ICoupon
from zope.interface import Interface


class IEasyShopCouponLayer(Interface):
    """ marker interface for browserlayer
    """

class ICouponManagement(Interface):
    """ marker for coupon management
    """
