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
from easyshop.core.interfaces import IBankAccount
from easyshop.payment.content import BankAccount

class BankAccountEditForm(base.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)    
    form_fields = form.Fields(IBankAccount)
    
    label       = _(u"Edit Bank Account")
    description = _("To change your bank information edit the form and press save.")
    form_name   = _(u"Edit Bank Account")

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
                    
class BankAccountAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IBankAccount)
    
    label     = _(u"Add Bank Information")
    form_name = _(u"Add Bank Information")

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
        id = self.context.generateUniqueId("BankAccount")

        direct_debit = BankAccount(id)
        direct_debit.account_number = data.get("account_number")
        direct_debit.bank_identification_code = data.get("bank_identification_code")
        direct_debit.depositor = data.get("depositor")
        direct_debit.bank_name = data.get("bank_name")
        
        self.context._setObject(id, direct_debit)

        direct_debit.reindexObject()
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
