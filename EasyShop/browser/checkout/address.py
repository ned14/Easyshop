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
from Products.EasyShop.interfaces import IPaymentManagement

class ICheckOutAddressView(Interface):
    """
    """        
    def getAddressInfo():
        """Returns address fields as dict.
        """

    def getCountries():
        """Returns countries as dict.
        """
        
class CheckOutAddressView(BrowserView):
    """
    """
    implements(ICheckOutAddressView)

    def getAddressInfo(self):
        """
        """
        id = self.request.get("id")
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        address = am.getAddress(id)
        
        result = {}
        result["id"] = id
         
        if self.request.get("firstname", "") != "":
            result["firstname"] = self.request.get("firstname")
        else:
            result["firstname"] = address.getFirstname()

        if self.request.get("lastname", "") != "":
            result["lastname"] = self.request.get("lastname")
        else:
            result["lastname"] = address.getLastname()

        if self.request.get("companyname", "") != "":
            result["companyname"] = self.request.get("companyname")
        else:
            result["companyname"] = address.getCompanyName()

        if self.request.get("address1", "") != "":
            result["address1"] = self.request.get("address1")
        else:
            result["address1"] = address.getAddress1()

        if self.request.get("address2", "") != "":
            result["address2"] = self.request.get("address2")
        else:
            result["address2"] = address.getAddress2()

        if self.request.get("zipcode", "") != "":
            result["zipcode"] = self.request.get("zipcode")
        else:
            result["zipcode"] = address.getZipCode()

        if self.request.get("city", "") != "":
            result["city"] = self.request.get("city")
        else:
            result["city"] = address.getCity()

        if self.request.get("country", "") != "":
            result["country"] = self.request.get("country")
        else:
            result["country"] = address.getCountry()

        if self.request.get("phone", "") != "":
            result["phone"] = self.request.get("phone")
        else:
            result["phone"] = address.getPhone()
            
        return result
            
    def getCountries(self):
        """
        """
        selected_country = self.request.get("country", "Deutschland")
        shop = self.context.getShop()
        
        result = []
        for country in shop.getCountries():
            result.append({
                "name" : country,
                "selected" : (selected_country == country)
            })
            
        return result    

        
