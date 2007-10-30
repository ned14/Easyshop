# zope imports
from zope.component import getMultiAdapter
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
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IShopManagement

class AddressEditForm(base.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(IAddress)
    
    label = _(u"Edit Address")
    description = _("To change your address edit the form and press save.")
    form_name = _(u"Edit Address")

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

        self.goto()

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        """
        """                
        zope.event.notify(EditCancelledEvent(self.context))        
        self.goto()

    def goto(self):
        """
        """
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:
            shop = IShopManagement(self.context).getShop()    
            url = "%s/manage-addressbook" % shop.absolute_url()
            self.request.response.redirect(url)
            
            
class AddressAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)    
    form_fields = form.Fields(IAddress)
    
    label = _(u"Add Address")
    form_name = _(u"Add Address")

    @form.action(_(u"label_save", default=u"Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        self.createAndAdd(data)
    
    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        url = "%s/manage-addressbook" % self.context.absolute_url()
        self.request.response.redirect(url)
    
    def createAndAdd(self, data):
        """
        """
        # get customer
        view = getMultiAdapter((self.context, self.context.REQUEST), name="checkOutView")
        customer = view.getAuthenticatedCustomer()

        # add address
        id = self.context.generateUniqueId("Address")

        customer.invokeFactory("Address", id=id, title=data.get("address1"))
        address = getattr(customer, id)

        # set data
        address.setFirstname(data.get("firstname", ""))
        address.setLastname(data.get("lastname", ""))
        address.setAddress1(data.get("address1", ""))
        address.setAddress2(data.get("address2", ""))
        address.setZipCode(data.get("zipCode", ""))
        address.setCity(data.get("city", ""))
        address.setCountry(data.get("country", ""))
        address.setPhone(data.get("phone", ""))
