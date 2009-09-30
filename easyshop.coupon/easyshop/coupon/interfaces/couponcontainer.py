from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from easyshop.coupon import couponMessageFactory as _

class ICouponContainer(Interface):
    """container for easyshop coupons"""
    
    # -*- schema definition goes here -*-
