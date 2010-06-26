""" patching redirectToNextURL because the coupon cookie has to be deleted here
"""
from easyshop.coupon.config import COUPON_COOKIE_NAME

def redirectToNextURL(obj, id):
    """Redirects to next URL by given id.
    """
    # expire coupon cookie
    if id in ['BUYED_ORDER', 'ASYNCHRONOUS_PAYMENT']:
        obj.context.REQUEST.RESPONSE.expireCookie(COUPON_COOKIE_NAME,path="/")

    # redirect to next url
    next_url = obj.getNextURL(id)
    obj.context.REQUEST.RESPONSE.redirect(next_url)
