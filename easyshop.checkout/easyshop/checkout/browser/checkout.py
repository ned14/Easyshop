# Zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import IShopManagement

class ICheckOutView(Interface):    
    """Provides methods for all checkout forms
    (Which are all in context of a shop content object)
    """    

    def checkOut():
        """
        """   

    def getAddressesPerLine():
        """Returns addresses of authenticated customer as lol.
        """

    def getAddressType():
        """Returns the type of the to selected address.
        
        Returns "invoice" resp. "shipping".
        """

    def getAuthenticatedCustomer():
        """Returns the authenticated customer.
        """

    def getCountries():
        """Returns countries as dict.
        """

    def customerHasAddresses():
        """Returns True if authenticated customer has addresses.
        """
        
    def getFirstname():
        """Returns the firstname of the customer. Takes it either from the 
        member object or from the address object.
        """

    def getGoto():
        """Returns the value of the variable goto
        """    

    def getLastname():
        """Returns the lastname of the customer. Takes it either from the 
        member object or from the address object.
        """

    def getSelectedInvoiceAddressAsString():
        """
        """

    def getSelectedShippingAddressAsString():
        """
        """
        
    def getSendToButtonValue():
        """Returns the proper value text for the send to button.
        """
        
    def isShippingAddress():
        """Returns true if the type of the to selected address is invoice.
        """
        
class CheckOutView(BrowserView):
    """
    """
    implements(ICheckOutView)

    def checkOut(self):
        """
        """   
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.isAnonymousUser():
            url = "%s/login_form?came_from=%s/check-out-addresses-goto" % (self.context.absolute_url(), self.context.absolute_url())
        else:
            url = "%s/check-out-addresses-goto" % self.context.absolute_url()

        return  self.context.request.response.redirect(url)

    def getAddressesPerLine(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        addresses = am.getAddresses()
        
        result = []
        line = []        
        for index, address in enumerate(addresses):

            line.append({
                "id"          : address.getId(),
                "firstname"   : address.getFirstname(),
                "lastname"    : address.getLastname(),
                "companyname" : address.getCompanyName(),
                "address1"    : address.getAddress1(),
                "address2"    : address.getAddress2(),
                "zipcode"     : address.getZipCode(),
                "city"        : address.getCity(),
                "country"     : address.getCountry(),
                "phone"       : address.getPhone(),
            })
            if (index + 1) % 3 == 0:
                result.append(line)
                line = []

        result.append(line)
        
        return result

    def getAddressType(self):
        """
        """
        return self.request.get("address_type", "shipping")

    def getAuthenticatedCustomer(self):
        """
        """
        cm = ICustomerManagement(self.context)
        return cm.getAuthenticatedCustomer()

    def getCountries(self):
        """
        """
        selected_country = self.request.get("country", "Deutschland")
        shop = IShopManagement(self.context).getShop()
        
        result = []
        for country in shop.getCountries():
            result.append({
                "name" : country,
                "selected" : (selected_country == country)
            })
            
        return result    

    def customerHasAddresses(self):
        """
        """
        cm = ICustomerManagement(IShopManagement(self.context).getShop())
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        return am.hasAddresses()
        
    def getFirstname(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        
        firstname = self.request.get("firstname", "")
        if firstname == "":
            m = mtool.getAuthenticatedMember()            
            firstname = m.getProperty("firstname")
        return firstname

    def getGoto(self):
        """
        """    
        return self.request.get("goto", None)

    def getLastname(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        
        lastname = self.request.get("lastname", "")
        if lastname == "":
            m = mtool.getAuthenticatedMember()            
            lastname = m.getProperty("lastname")
        return lastname
                    
    def getSelectedInvoiceAddressAsString(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        return customer.getInvoiceAddressAsString()
        
    def getSelectedShippingAddressAsString(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        return customer.getShippingAddressAsString()
                
    def getSendToButtonValue(self):
        """
        """
        if self.getAddressType() == "invoice":
            return "Send invoice to this address"            
        else:
            return "Send products to this address"
        
    def isShippingAddress(self):
        """
        """
        return self.getAddressType() == "shipping"        

