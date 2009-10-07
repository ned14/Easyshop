"""Definition of the Coupon content type
"""

from random import choice

from zope.interface import implements

from Products.Archetypes import atapi

from easyshop.coupon import couponMessageFactory as _
from easyshop.coupon.interfaces import ICoupon
from easyshop.coupon.config import PROJECTNAME, COUPON_ID_PATTERN, \
                                   COUPON_ID_LENGTH

schema = atapi.BaseSchema.copy() + atapi.Schema((

    atapi.StringField('title',
        widget=atapi.StringWidget(
            visible={'edit':'invisible', 'view':'invisible'},
        ),
        required=False
    ),

    atapi.StringField('couponId',
        default_method='generate_cid',
        required=True,
        widget=atapi.StringWidget(
            label=_('coupon ID'),
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

schema.changeSchemataForField('effectiveDate','default')
schema.changeSchemataForField('expirationDate','default')

class Coupon(atapi.BaseContent):
    """easyshop coupon"""
    implements(ICoupon)
    _at_rename_after_creation = True
    schema = schema.copy()

    def generate_cid(self):
        return ''.join([choice(COUPON_ID_PATTERN) for i
                        in range(COUPON_ID_LENGTH)])

    def Title(self):
        return "Coupon Code: %s" % self.getCouponId()

    def getValue(self):
        value = []

        if self.effective:
            value.append(
                _("coupon_effective", mapping=dict(effective=self.effective)))

        if self.expires:
            value.append(
                _("coupon_expires", mapping=dict(expires=self.expires)))

        return ','.join(value)

atapi.registerType(Coupon, PROJECTNAME)
