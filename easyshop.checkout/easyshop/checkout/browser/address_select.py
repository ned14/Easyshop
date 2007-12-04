# zope imports
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# easyshop.core imports 
from easyshop.core.config import _
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop


class IAddressSelectForm(Interface):
    """
    """
    invoice_address  = schema.TextLine()
    shipping_address = schema.TextLine()
    
class ShopAddressSelectForm:
    """
    """
    implements(IAddressSelectForm)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        
    invoice_address  = u""
    shipping_address = u""


# Using here Five's EditForm by heart because plone.app.form would lock the shop 
# which is not desired in this case (because the shop is not modified at all)
class AddressSelectForm(formbase.EditForm):
    """
    """ 
    template = pagetemplatefile.ZopeTwoPageTemplateFile("address_select.pt")
    form_fields = form.Fields(IAddressSelectForm)

    @form.action(_(u"label_next", default="Next"), condition=form.haveInputWidgets, name=u'next')
    def handle_next_action(self, action, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        customer.selected_invoice_address  = data.get("invoice_address", "")
        customer.selected_shipping_address = data.get("shipping_address", "")
        
        ICheckoutManagement(self.context).redirectToNextURL("SELECTED_ADDRESSES")

    @form.action(_(u"label_add_address", default="Add Address"), name=u'add_address')
    def handle_add_address_action(self, action, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        customer_url = customer.absolute_url()
        template_url = self.context.absolute_url() + "/checkout-select-addresses"
        
        url = customer_url + "/add-address?goto=" + template_url
        self.request.response.redirect(url)
        
    def getShippingAddresses(self):
        """Returns all addresses with the currently selected invoice address
        checked.
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)

        found_selected_address = False
        result = []
        line = []

        for index, address in enumerate(am.getAddresses()):

            checked = False
            if safe_unicode(address.getId()) == customer.selected_shipping_address:
                checked = "checked"
                found_selected_address = True

            address_as_dict = self._getAddressAsDict(address)
            address_as_dict["checked"] = checked
            
            line.append(address_as_dict)
            
            if (index + 1) % 3 == 0:
                result.append(line)
                line = []
                
        result.append(line)
        
        if len(result) > 0 and found_selected_address == False:
            result[0][0]["checked"] = True

        return result
        
    def getInvoiceAddresses(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)

        found_selected_address = False
        result = []
        line = []

        for index, address in enumerate(am.getAddresses()):

            checked = False
            if safe_unicode(address.getId()) == customer.selected_invoice_address:
                checked = "checked"
                found_selected_address = True

            address_as_dict = self._getAddressAsDict(address)
            address_as_dict["checked"] = checked
            
            line.append(address_as_dict)
            
            if (index + 1) % 3 == 0:
                result.append(line)
                line = []
                
        result.append(line)
        
        if found_selected_address == False:
            result[0][0]["checked"] = True

        return result

    def _getAddressAsDict(self, address):
        """Returns given address as dictionary.
        """
        return {
            "id"          : address.getId(),
            "url"         : address.absolute_url(),
            "firstname"   : address.firstname,
            "lastname"    : address.lastname,
            "companyname" : address.company_name,
            "address1"    : address.address_1,
            "zipcode"     : address.zip_code,
            "city"        : address.city,
            "country"     : address.country,
            "phone"       : address.phone,
            }