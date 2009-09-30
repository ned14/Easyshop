from zope import interface, schema
from z3c.form import form, field, button
from plone.z3cform import layout
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from easyshop.coupon import couponMessageFactory as _


class ICouponCodeForm(interface.Interface):

    coupon_code = schema.ASCIILine(
        title = _("coupon code"),
    )


class CouponCodeForm(form.Form):
    """
    """
    fields = field.Fields(ICouponCodeForm)
    ignoreContext = True
    label = _(u"If you have a Coupon Code please enter it hereas")

    @button.buttonAndHandler(_("apply code"))
    def apply_code(self,action):
        data, errors = self.extractData()
        # stuff to do
        pass


class CouponCodeFormViewlet(ViewletBase, layout.FormWrapper):
    """
    """
    index = ViewPageTemplateFile('couponcode_viewlet.pt')
    form = CouponCodeForm

    def __init__(self, *args):
        super(CouponCodeFormViewlet, self).__init__(*args)
        if self.form is not None:
            self.form_instance = self.form(self.context.aq_inner, self.request)
            self.form_instance.__name__ = self.__name__
