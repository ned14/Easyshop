# zope imports
from zope.formlib import form
import zope.event
import zope.lifecycleevent


from Products.Five.browser import pagetemplatefile

# plone imports
from plone.app.form import base
from plone.app.form.validators import null_validator
from plone.app.form.events import EditCancelledEvent, EditSavedEvent

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import IDirectDebit
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

class DirectDebitEditForm(base.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)    
    form_fields = form.Fields(IDirectDebit)
    
    label = _(u"Edit Bank Information")
    description = _("To change your bank information edit the form and press save.")
    form_name = _(u"Edit Bank Information")

    @form.action(_(u"label_save", default="Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            zope.event.notify(EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            zope.event.notify(EditCancelledEvent(self.context))
            self.status = "No changes"

        # Return to overview
        shop = IShopManagement(self.context).getShop()
        url = "%s/manage-payment-methods" % shop.absolute_url()
        self.request.response.redirect(url)

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        """
        """                
        zope.event.notify(EditCancelledEvent(self.context))
        
        # Return to overview
        shop = IShopManagement(self.context).getShop()
        url = "%s/manage-payment-methods" % shop.absolute_url()
        self.request.response.redirect(url)
        
class DirectDebitAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IDirectDebit)
    
    label = _(u"Add Bank Information")
    form_name = _(u"Add Bank Information")

    @form.action(_(u"label_save", default=u"Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        self.createAndAdd(data)
    
    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        url = "%s/manage-payment-methods" % self.context.absolute_url()
        self.request.response.redirect(url)
    
    def createAndAdd(self, data):
        """
        """
        # get customer
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()

        # add address
        id = self.context.generateUniqueId("DirectDebit")

        customer.invokeFactory("DirectDebit", id=id, title=data.get("address1"))
        direct_debit = getattr(customer, id)

        # set data
        direct_debit.setAccountNumber(data.get("accountNumber"))
        direct_debit.setBankIdentificationCode(data.get("bankIdentificationCode"))
        direct_debit.setName(data.get("name"))
        direct_debit.setBankName(data.get("bankName"))

        # Return to overview
        url = "%s/manage-payment-methods" % self.context.absolute_url()
        self.request.response.redirect(url)

