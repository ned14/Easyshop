# zope imports
from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectModifiedEvent

from Products.Five.browser import pagetemplatefile

# plone imports
from plone.app.form import base
from plone.app.form.validators import null_validator
from plone.app.form.events import EditCancelledEvent, EditSavedEvent

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import ICreditCard
from easyshop.payment.content.credit_card import CreditCard

class CreditCardEditForm(base.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)    
    form_fields = form.Fields(ICreditCard)
    
    label       = _(u"Edit Credit Card")
    description = _("To change your credit card edit the form and press save.")
    form_name   = _(u"Edit Credit Card")

    @form.action(_(u"label_save", default="Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            notify(EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            notify(EditCancelledEvent(self.context))
            self.status = "No changes"

        self.context.reindexObject()
        self.nextUrl()

    @form.action(_(u"label_cancel", default=u"Cancel"), validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, action, data):
        """
        """                
        notify(EditCancelledEvent(self.context))
        self.nextUrl()
        
    def nextUrl(self):
        """
        """
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:
            parent = self.context.aq_inner.aq_parent
            url = parent.absolute_url() + "/manage-payment-methods"
            self.request.response.redirect(url)
                    
class CreditCardAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(ICreditCard)
    
    label     = _(u"Add Credit Card")
    form_name = _(u"Add Credit Card")

    @form.action(_(u"label_save", default=u"Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)
    
    @form.action(_(u"label_cancel", default=u"Cancel"), validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, action, data):
        """
        """
        self.context.reindexObject()
        self.nextUrl()
    
    def createAndAdd(self, data):
        """
        """
        # add address
        id = self.context.generateUniqueId("CreditCard")

        credit_card = CreditCard(id)
        credit_card.card_type                  = data.get("card_type")
        credit_card.card_owner                 = data.get("card_owner")
        credit_card.card_number                = data.get("card_number")
        credit_card.card_expiration_date_month = data.get("card_expiration_date_month")
        credit_card.card_expiration_date_year  = data.get("card_expiration_date_year")
        
        self.context._setObject(id, credit_card)

        credit_card.reindexObject()
        self.nextUrl()

    def nextUrl(self):
        """
        """
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:
            url = self.context.absolute_url() + "/manage-payment-methods"
            self.request.response.redirect(url)
