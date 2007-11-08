# zope imports
from zope.formlib import form

from Products.Five.browser import pagetemplatefile

# plone imports
from plone.app.form import base

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement

class AddressAddForm(base.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("address_form.pt")
    form_fields = form.Fields(IAddress)
    
    label = _(u"Add Address")
    form_name = _(u"Add Address")

    @form.action(_(u"label_save", default=u"Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)
        ICheckoutManagement(self.context).redirectToNextURL("ADDED_ADDRESS")
    
    def createAndAdd(self, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        am.addAddress(data)

    def getAddressType(self):
        """
        """
        return self.request.get("address_type", "shipping")
        
    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == "shipping"