"""Common configuration constants
"""
from string import letters

PROJECTNAME = 'easyshop.coupon'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Coupon': 'easyshop.coupon: Add Coupon',
    'CouponContainer': 'easyshop.coupon: Add CouponContainer',
}

COUPON_ID_PATTERN = letters
COUPON_ID_LENGTH = 10
COUPON_COOKIE_NAME = "easyshop-couponcode"
COUPON_COOKIE_DURATION_SEC = 900 # cookie is 15 min valid

