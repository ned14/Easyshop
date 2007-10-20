# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.utils import shasattr

# EasyShop imports
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICustomer

class CustomerAddressManager:
    """An adapter which provides address management for customers.
    """
    implements(IAddressManagement)
    adapts(ICustomer)

    def __init__(self, context):
        self.context = context                  

    def addAddress(self, a1, a2, z, ci, co):
        """
        """
        id = self.context.generateUniqueId("Address")
        self.context.invokeFactory("Address", id=id, title=a1)
                
        address = getattr(self.context, id)
        address.setAddress1(a1)
        address.setAddress2(a2)
        address.setZipCode(z)
        address.setCity(ci)
        address.setCountry(co)
        
        return id
        
    def deleteAddress(self, id):
        """
        """
        try:
            self.context.manage_delObjects(id)
        except AttributeError:
            return False
        
        return True

    def getAddress(self, id):
        """
        """
        return getattr(self.context, id, None)
        
    def getAddresses(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Address",
            path = "/".join(self.context.getPhysicalPath())
        )
        
        return [brain.getObject() for brain in brains]

    def getInvoiceAddress(self):
        """
        """
        if shasattr(self.context, self.context.getInvoiceAddressAsString()):
            return getattr(self.context, self.context.getInvoiceAddressAsString())

        try:    
            return self.getAddresses()[0]
        except IndexError:
            return None

    def getShippingAddress(self):
        """
        """
        if shasattr(self.context, self.context.getShippingAddressAsString()):
            return getattr(self.context, self.context.getShippingAddressAsString())
        
        try:    
            return self.getAddresses()[0]
        except IndexError:
            return None

    def hasAddresses(self):
        """
        """
        return len(self.getAddresses()) > 0
            
            