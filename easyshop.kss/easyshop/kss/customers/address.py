# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# easyshop.core imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShopManagement

from snippets import ADDRESS_ADD_FORM

class AddressKSSView(PloneKSSView):
    """
    """
    @kssaction    
    def showAddAddressForm(self):
        """
        """
        kss_core  = self.getCommandSet("core")

        html = ADDRESS_ADD_FORM
        
        # refresh cart
        kss_core  = self.getCommandSet("core")
        kss_core.replaceHTML('#add-address-form', html)
        
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
        address.setAddress1(form.get("address1", ""))
        address.setAddress2(form.get("address2", ""))
        address.setZipCode(form.get("zipCode", ""))
        address.setCity(form.get("city", ""))
        address.setCountry(form.get("country", ""))
        address.setPhone(form.get("phone", ""))

        # refresh product
        kss_core = self.getCommandSet("core")
        kss_zope = self.getCommandSet("zope")

        selector = kss_core.getHtmlIdSelector("manage-address-book")        
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.manager.addresses",
                                name="easyshop.addresses")