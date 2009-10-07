"""Definition of the Coupon content type
"""

import zope.i18n

from random import choice

from zope.interface import implements

from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName

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
        ts = getToolByName(self,'translation_service')

        if self.getEffectiveDate():
            localized_effective = ts.ulocalized_time(self.getEffectiveDate(),
                                                     context=self,
                                                     request=self.REQUEST)
            value.append(zope.i18n.translate(
                _("coupon_effective",
                  mapping=dict(date=localized_effective)),
                target_language=self.REQUEST.get('LANGUAGE','de')))

        if self.getExpirationDate():
            localized_expires = ts.ulocalized_time(self.getExpirationDate(),
                                                   context=self,
                                                   request=self.REQUEST)
            value.append(zope.i18n.translate(
                _("coupon_expires",
                  mapping=dict(date=localized_expires)),
                target_language=self.REQUEST.get('LANGUAGE','de')))

        return ', '.join(value)

atapi.registerType(Coupon, PROJECTNAME)
