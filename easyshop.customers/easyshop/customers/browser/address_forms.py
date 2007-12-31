# zope imports
from zope.formlib import form
from zope.event import notify
from zope.app.event.objectevent import ObjectModifiedEvent

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement

class AddressEditForm(formbase.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IAddress).omit("email")
    
    label = _(u"Edit Address")
    description = _("To change your address edit the form and press save.")
    form_name = _(u"Edit Address")

    @form.action(_(u"label_save", default="Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            # notify(EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            # notify(EditCancelledEvent(self.context))
            self.status = "No changes"

        self.context.reindexObject()
        self.context.aq_inner.aq_parent.reindexObject()

        self.redirectToNextURL()

    @form.action(_(u"label_cancel", default=u"Cancel"), name=u'cancel')    
    # validator=null_validator,     
    
    def handle_cancel_action(self, action, data):
        """
        """                
        # notify(EditCancelledEvent(self.context))        
        self.redirectToNextURL()

    def redirectToNextURL(self):
        """
        """        
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:
            customer = self.context.aq_inner.aq_parent
            url = "%s/manage-addressbook" % customer.absolute_url()
            self.request.response.redirect(url)
            
            
class AddressAddForm(formbase.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)    
    form_fields = form.Fields(IAddress).omit("email")
    
    label = _(u"Add Address")
    form_name = _(u"Add Address")

    @form.action(_(u"label_save", default=u"Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)
    
    @form.action(_(u"label_cancel", default=u"Cancel"), name=u'cancel')
    # validator=null_validator,
     
    def handle_cancel_action(self, action, data):
        """
        """
        self.redirectToNextURL()
    
    def createAndAdd(self, data):
        """
        """
        am = IAddressManagement(self.context)
        am.addAddress(data)
        
        self.redirectToNextURL()
        
    def redirectToNextURL(self):
        """
        """
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:            
            url = "%s/manage-addressbook" % self.context.absolute_url()
            self.request.response.redirect(url)
