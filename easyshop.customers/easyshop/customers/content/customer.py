# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer

class Customer(BaseFolder):
    """A customer can buy products from a shop. A customer has addresses and 
    payment methods.

    A customer exists additionally to the members of Plone. Whenever a member 
    wants to buy something a customer content object is added for this member. 
    This is intended to be changed to "remember" in future.
    """    
    implements(ICustomer)
    
    selected_invoice_address     = u""
    selected_shipping_address    = u""
    selected_payment_method      = u"prepayment"
    selected_payment_information = u""
    selected_shipping_method     = u"default"
    selected_country             = u""
    
    def __init__(self, id):
        """
        """
        super(Customer, self).__init__(id)
        self.selected_country = u"Deutschland"

    def Title(self):
        """
        """
        if self.firstname and self.lastname:
            return self.firstname + " " + self.lastname
        else:
            return self.getId()
    
    def SearchableText(self):
        """
        """
        text = []
        
        text.append(self.firstname)
        text.append(self.lastname)
        text.append(self.email)
        
        am = IAddressManagement(self)
        for address in am.getAddresses():
            if address.firstname:
                text.append(address.firstname)
            if address.lastname:
                text.append(address.lastname)
            if address.address_1:
                text.append(address.address_1)
            if address.zip_code:
                text.append(address.zip_code)            
            if address.city:
                text.append(address.city)
            if address.country:
                text.append(address.country)
                        
        return " ".join(text)

registerType(Customer, PROJECTNAME) 