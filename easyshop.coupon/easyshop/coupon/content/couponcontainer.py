"""Definition of the CouponContainer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi

from easyshop.coupon.interfaces import ICouponContainer
from easyshop.coupon.config import PROJECTNAME


class CouponContainer(atapi.OrderedBaseFolder):
    """container for easyshop coupons"""
    implements(ICouponContainer)


atapi.registerType(CouponContainer, PROJECTNAME)
