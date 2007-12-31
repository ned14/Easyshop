# zope imports
from zope.event import notify
from zope.formlib import form
from zope.app.event.objectevent import ObjectModifiedEvent

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import IShopManagement

class AddressEditForm(formbase.EditForm):
    """This form let anonymous users edit their already entered invoice and 
    shipping address. This happens when they click checkout again and they have 
    already entered addresses within the same sessions. 
    """
    
    template = pagetemplatefile.ZopeTwoPageTemplateFile("address_form.pt")
    form_fields = form.Fields(IAddress)

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

        shop = IShopManagement(self.context).getShop()
        ICheckoutManagement(shop).redirectToNextURL("EDITED_ADDRESS")

    def getAddressType(self):
        """
        """
        return self.request.get("address_type", "shipping")

    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == "shipping"

