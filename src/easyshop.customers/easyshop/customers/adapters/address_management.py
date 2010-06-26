# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import BadRequest

# Archetypes imports
from Products.Archetypes.utils import shasattr

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer
from easyshop.customers.content.address import Address

class CustomerAddressManager:
    """An adapter which provides address management for customers.
    """
    implements(IAddressManagement)
    adapts(ICustomer)

    def __init__(self, context):
        self.context = context                  

    def addAddress(self, data):
        """
        """
        id = self.context.generateUniqueId("Address")
        address = Address(id)

        address.firstname    = data.get("firstname", u"")
        address.lastname     = data.get("lastname", u"")
        address.company_name = data.get("company_name", u"")            
        address.address_1    = data.get("address_1", u"")            
        address.zip_code     = data.get("zip_code", u"")
        address.city         = data.get("city", u"")            
        address.country      = data.get("country", u"")
        address.phone        = data.get("phone", u"")
        address.email        = data.get("email", u"")
        
        self.context._setObject(id, address)
        
        if data.get("address_type", "") == "shipping":
            self.context.selected_shipping_address = id
        else:
            self.context.selected_invoice_address = id
            
        return id
        
    def deleteAddress(self, id):
        """
        """
        try:
            self.context.manage_delObjects(id)
        except BadRequest:
            return False
        
        return True

    def getAddress(self, id):
        """
        """
        return getattr(self.context, id, None)
        
    def getAddresses(self):
        """
        """
        return self.context.objectValues("Address")

    def getInvoiceAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_invoice_address):
            return getattr(self.context, self.context.selected_invoice_address)

        try:    
            return self.getAddresses()[0]
        except IndexError:
            return None

    def getShippingAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_shipping_address):
            return getattr(self.context, self.context.selected_shipping_address)
        
        try:    
            return self.getAddresses()[0]
        except IndexError:
            return None

    def hasAddresses(self):
        """
        """
        return len(self.getAddresses()) > 0
        
    def hasInvoiceAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_invoice_address):
            return True
        else:
            return False

    def hasShippingAddress(self):
        """
        """
        if shasattr(self.context, self.context.selected_shipping_address):
            return True
        else:
            return False        