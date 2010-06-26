from base64 import encodestring, decodestring
from urllib import quote, unquote
from datetime import datetime, timedelta

from zope.interface import implements
from zope.component import adapts, getMultiAdapter

from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IShop

from easyshop.coupon import couponMessageFactory as _
from easyshop.coupon.config import COUPON_COOKIE_NAME, \
    COUPON_COOKIE_DURATION_SEC
from easyshop.coupon.interfaces import ICouponManagement
from easyshop.coupon.interfaces import ICoupon


class CouponManagement:
    """
    """
    implements(ICouponManagement)
    adapts(IShop)

    def __init__(self, shop):
        """
        """
        self.shop = shop

    def saveCouponConsumer(self, couponId):
        """
        """
        customer = ICustomerManagement(self.shop).getAuthenticatedCustomer()

        if customer is None:
            raise Exception, "invalid customer"

        coupon = self.getCoupon(couponId)

        if not coupon:
            raise Exception, "no coupon found"

        old_consumers = coupon.getConsumers()
        if customer.id not in old_consumers:
            # add customer to consumers
            coupon.setConsumers(old_consumers + (customer.id, ))

            # set cookie for checkout
            expires = datetime.now() + \
                timedelta(seconds=COUPON_COOKIE_DURATION_SEC)

            self.shop.REQUEST.RESPONSE.setCookie(
                COUPON_COOKIE_NAME,
                quote(encodestring(couponId)),
                path='/',
                expires=expires
            )

        else:
            raise Exception, "coupon already consumed"

    def getCoupon(self, couponId):
        """
        """
        catalog = getMultiAdapter((self.shop, self.shop.REQUEST),
                                  name="plone_tools").catalog()

        coupons = catalog(
            portal_type="Coupon",
            getCouponId=couponId)

        return len(coupons)>0 and coupons[0].getObject() or None

    def getValidCoupon(self, check_coupon=None):
        """
        """
        stored_coupon_id = self.shop.REQUEST.get(COUPON_COOKIE_NAME)

        if not stored_coupon_id:
            return

        coupon_id = decodestring(unquote(stored_coupon_id))
        coupon = self.getCoupon(coupon_id)

        if check_coupon is not None:
            if coupon!=check_coupon:
                return

        customer = ICustomerManagement(self.shop).getAuthenticatedCustomer()

        if customer and \
           customer.id in coupon.getConsumers():
            return coupon

        return

# messagefactories for i18ndude
_("invalid customer")
_("no coupon found")
_("coupon already consumed")
