"""Definition of the Coupon content type
"""

from random import choice

from zope.interface import implements

from Products.Archetypes import atapi

from easyshop.coupon import couponMessageFactory as _
from easyshop.coupon.interfaces import ICoupon
from easyshop.coupon.config import PROJECTNAME, COUPON_ID_PATTERN, \
                                   COUPON_ID_LENGTH

CouponSchema = atapi.OrderedBaseFolderSchema.copy() + atapi.Schema((

    atapi.StringField('couponId',
        default_method='generate_cid',
        required=True,
        widget=atapi.StringWidget(
            label=_('coupon ID'),
        ),
    ),
    
    atapi.FloatField('discount',
        widget=atapi.StringWidget(
            label=_('coupon discount'),
            description=_('discount value as percent or amount'),
        ),
    ),
    
    atapi.BooleanField('isPercentage',
        widget=atapi.BooleanWidget(
            label=_('coupon discount value is percentage'),
        ),
    ),
    
    atapi.LinesField('consumers',
        widget=atapi.LinesWidget(
            visible=dict(
                view='visible',
                edit='hidden',
            ),
        ),
    ),
))

CouponSchema.changeSchemataForField('effectiveDate','default')
CouponSchema.changeSchemataForField('expirationDate','default')

CouponSchema.moveField('couponId',before='title')

class Coupon(atapi.OrderedBaseFolder):
    """easyshop coupon"""
    implements(ICoupon)
    _at_rename_after_creation = True
    schema = CouponSchema

    def generate_cid(self):
        return ''.join([choice(COUPON_ID_PATTERN) for i 
                        in range(COUPON_ID_LENGTH)])
        
atapi.registerType(Coupon, PROJECTNAME)
