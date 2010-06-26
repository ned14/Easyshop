from Acquisition import aq_inner
from zope.interface import implements, Interface
from zope.app.pagetemplate import ViewPageTemplateFile

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from easyshop.coupon import couponMessageFactory as _


class ICouponsView(Interface):
    """
    coupons view interface
    """


class CouponsView(BrowserView):
    """
    coupons browser view
    """
    implements(ICouponsView)

    def getCoupons(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context,'portal_catalog')
        coupons = ()
        
        for coupon in context.getFolderContents(full_objects=True):
            coupons += (dict(
                title=coupon.Title(),
                url=coupon.absolute_url(),
                amount_of_criteria=len(coupon.objectIds()),
            ),)
        
        return coupons
