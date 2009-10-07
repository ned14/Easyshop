from Acquisition import aq_inner

from zope import interface, schema, component
from z3c.form import form, field, button

from plone.z3cform import layout
from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from easyshop.coupon.interfaces import ICouponManagement
from easyshop.coupon import couponMessageFactory as _


class ICouponCodeForm(interface.Interface):

    couponId = schema.ASCIILine(
        title = _("coupon code"),
        required = False,
    )

class CouponCodeForm(form.Form):
    """
    """
    fields = field.Fields(ICouponCodeForm)
    ignoreContext = True
    label = _(u"If you have a Coupon Code please enter it here")

    @button.buttonAndHandler(_("apply code"))
    def apply_code(self,action):
        data, errors = self.extractData()
        coupon_id = data.get('couponId','')
        context = aq_inner(self.context)
        cm = ICouponManagement(context)
        sm = IStatusMessage(self.request)

        if not coupon_id:
            self.status = _("please enter a valid coupon id")
            return

        try:
            cm.saveCouponConsumer(coupon_id.strip())
            sm.addStatusMessage(_("valid coupon consumed"))

            template_id = component.getMultiAdapter(
                (self.context,self.request),
                name="plone_context_state").current_page_url().split('/').pop()

            return self.request.response.redirect(template_id)
        except Exception, msg:
            # see easyshop.coupon.adapters.coupon_management for exceptions
            self.status = msg


class CouponCodeFormViewlet(ViewletBase, layout.FormWrapper):
    """
    """
    index = ViewPageTemplateFile('couponcode_viewlet.pt')
    form = CouponCodeForm

    def __init__(self, *args):
        """
        """
        super(CouponCodeFormViewlet, self).__init__(*args)
        if self.form is not None:
            self.form_instance = self.form(self.context.aq_inner, self.request)
            self.form_instance.__name__ = self.__name__

    def get_coupon(self):
        """
        """
        cm = ICouponManagement(self.context)
        return cm.getValidCoupon()

