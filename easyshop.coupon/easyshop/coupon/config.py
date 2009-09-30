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
