# Five imports
from Products.Five.browser import BrowserView

# easyshop.core imports 
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement

class AddressSelectForm(BrowserView):
    """
    """
    
    def getAddressesPerLine(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        addresses = am.getAddresses()
        
        result = []
        line = []        
        for index, address in enumerate(addresses):

            line.append({
                "id"          : address.getId(),
                "firstname"   : address.firstname,
                "lastname"    : address.lastname,
                "companyname" : address.company_name,
                "address1"    : address.address_1,
                "address2"    : address.address_2,
                "zipcode"     : address.zip_code,
                "city"        : address.city,
                "country"     : address.country,
                "phone"       : address.phone,
            })
            if (index + 1) % 3 == 0:
                result.append(line)
                line = []

        result.append(line)
        
        return result

    def getGoto(self):
        """
        """    
        return self.request.get("goto", None)
        
    def getSelectedInvoiceAddressAsString(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        return customer.invoiceAddressAsString
        
    def getSelectedShippingAddressAsString(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        return customer.shippingAddressAsString
                
    def getAddressType(self):
        """
        """
        return self.request.get("address_type", "shipping")
        
    def selectAddresses(self):
        """
        """
        selected_shipping_address = self.request.get("selected_shipping_address")
        selected_invoice_address  = self.request.get("selected_invoice_address")
        
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()

        # set addresses
        customer.shippingAddressAsString = selected_shipping_address
        customer.invoiceAddressAsString  = selected_invoice_address

        url = "%s/select-shipping-form" % self.context.absolute_url()
        
        self.context.request.response.redirect(url)