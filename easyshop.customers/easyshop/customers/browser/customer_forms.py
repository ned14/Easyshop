# zope imports
from zope.formlib import form
import zope.event
import zope.lifecycleevent

# Five imports
from Products.Five.browser import pagetemplatefile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.app.form import base
from plone.app.form.validators import null_validator
from plone.app.form.events import EditCancelledEvent, EditSavedEvent

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import DEFAULT_SHOP_FORM
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IShopManagement

class CustomerEditForm(base.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile(DEFAULT_SHOP_FORM)
    form_fields = form.Fields(ICustomer)
    
    label = _(u"Edit Customer")
    description = _("Please edit the form below and press save.")
    form_name = _(u"Edit Customer")

    @form.action(_(u"label_save", default="Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        utils = getToolByName(self.context, "plone_utils")
        utils.addPortalMessage(_(u"Changes saved"), "info")
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            zope.event.notify(EditSavedEvent(self.context))
        else:
            zope.event.notify(EditCancelledEvent(self.context))

        self.context.reindexObject()
        self._nextUrl()
        
    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        """
        """
        utils = getToolByName(self.context, "plone_utils")
        utils.addPortalMessage(_(u"Edit canceled"), "info")
        
        zope.event.notify(EditCancelledEvent(self.context))        
        self._nextUrl()        

    def _nextUrl(self):
        """
        """
        url = self.request.get("goto", "")
        if url != "":
            self.request.response.redirect(url)
        else:
            url =  self.context.absolute_url()
            url += "/my-account"
            self.request.response.redirect(url)
            