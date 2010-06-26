# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.core imports
from easyshop.core.config import MESSAGES
from easyshop.core.config import _
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

from snippets import *

class AddressKSSView(PloneKSSView):
    """
    """
    @kssaction    
    def showAddAddressForm(self):
        """
        """
        html = self._getAddAddressForm()
        
        # refresh cart
        kss_core  = self.getCommandSet("core")
        kss_core.replaceHTML('#add-address-form', html)

    @kssaction    
    def showEditAddressForm(self, form):
        """
        """        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = form.get("uid", "")
        )
        
        try: 
            address = brains[0].getObject()
        except:
            return 
        
        html = "<tr>"
        html += self._getEditAddressForm(address)
        html += "</tr>"
        
        # refresh cart
        kss_core  = self.getCommandSet("core")
        kss_core.replaceHTML("#%s" % address.UID(), html)
        
    @kssaction    
    def addAddress(self, form):
        """
        """
        shop = IShopManagement(self.context).getShop()
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()
        
        id = self.context.generateUniqueId("Address")

        customer.invokeFactory("Address", id=id, title=form.get("address1"))
        address = getattr(customer, id)

        # set data
        address.setFirstname(form.get("firstname", ""))
        address.setLastname(form.get("lastname", ""))
        address.setLastname(form.get("companyName", ""))
        address.setAddress1(form.get("address1", ""))
        address.setAddress2(form.get("address2", ""))
        address.setZipCode(form.get("zipCode", ""))
        address.setCity(form.get("city", ""))
        address.setCountry(form.get("country", ""))
        address.setPhone(form.get("phone", ""))

        # Refresh addresses
        kss_core = self.getCommandSet("core")
        kss_zope = self.getCommandSet("zope")

        selector = kss_core.getHtmlIdSelector("manage-address-book")        
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.manager.addresses",
                                name="easyshop.addresses")

    @kssaction    
    def editAddress(self, form):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = form.get("uid", "")
        )
        
        try: 
            address = brains[0].getObject()
        except:
            return 
                
        # set data
        address.setFirstname(form.get("firstname", ""))
        address.setLastname(form.get("lastname", ""))
        address.setLastname(form.get("companyName", ""))
        address.setAddress1(form.get("address1", ""))
        address.setAddress2(form.get("address2", ""))
        address.setZipCode(form.get("zipCode", ""))
        address.setCity(form.get("city", ""))
        address.setCountry(form.get("country", ""))
        address.setPhone(form.get("phone", ""))

        # Refresh addresses
        kss_core = self.getCommandSet("core")
        kss_zope = self.getCommandSet("zope")

        selector = kss_core.getHtmlIdSelector("manage-address-book")        
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.manager.addresses",
                                name="easyshop.addresses")

    @kssaction    
    def cancelAddress(self):
        """
        """
        # Refresh addresses
        kss_core = self.getCommandSet("core")
        kss_zope = self.getCommandSet("zope")

        selector = kss_core.getHtmlIdSelector("manage-address-book")
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.manager.addresses",
                                name="easyshop.addresses")

    def _getAddAddressForm(self):
        """
        """
        html  = """<h1>%s</h1>""" % _(u"Add Address")
        html += """<div class="description">%s</div>""" % _(u"Please enter a new address and click save.")
        html += FORM_HEADER("add-address-form")
        
        html += FORM_TEXT_FIELD("Firstname", "firstname", True)
        html += FORM_TEXT_FIELD("Lastname", "lastname", True)
        html += FORM_TEXT_FIELD("Company Name", "companyName", False)
        html += FORM_TEXT_FIELD("Address 1", "address1", True)
        html += FORM_TEXT_FIELD("Zip Code", "zipCode", True)
        html += FORM_TEXT_FIELD("City", "city", True)
        html += FORM_TEXT_FIELD("Phone", "phone", False)
        html += FORM_BUTTON(id="add-address")
        html += FORM_BUTTON(id="cancel-address", value="Cancel", klass="standalone")
        html += FORM_FOOTER()
        
        return html
        
    def _getEditAddressForm(self, address):
        """
        """
        html  = FORM_HEADER("edit-address-form")
        html += """<input type="hidden" name="uid" value="%s" />""" % address.UID()
        html += FORM_TEXT_FIELD("Firstname", "firstname", True, address.getFirstname())
        html += FORM_TEXT_FIELD("Lastname", "lastname", True, address.getLastname())
        html += FORM_TEXT_FIELD("Company Name", "companyName", False, address.getCompanyName())
        html += FORM_TEXT_FIELD("Address 1", "address1", True, address.getAddress1())
        html += FORM_TEXT_FIELD("Zip Code", "zipCode", True, address.getZipCode())
        html += FORM_TEXT_FIELD("City", "city", True, address.getCity())
        html += FORM_TEXT_FIELD("Phone", "phone", False, address.getPhone())
                    
        html += FORM_BUTTON(id="edit-address")
        html += FORM_BUTTON(id="cancel-address", value="Cancel", klass="standalone")
        html += FORM_FOOTER()
        
        return html