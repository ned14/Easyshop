# zope imports
from zope.interface import Interface

################################################################################
# Address
################################################################################
        
class IAddress(Interface):
    """A address.
    """
    
class IAddressManagement(Interface):
    """Provides methods to manage address content objects.
    """
    def addAddress(a1, a2, z, ci, co):
        """Adds an address.
            
           Parameters:    
               a1 = address 1
               a2 = address 2
               z  = zipcode
               ci = city
               co = country           
        """
        
    def deleteAddress(id):
        """Deletes an address by given id.
        """

    def getAddress(id):
        """Returns address by given id. If it isn't exist returns None.
        """
        
    def getAddresses():
        """Returns all addresses.
        """

    def getEmailAddress():
        """Returns the email address of an customer.
        Which is saved in the corresponding member.
        """
        
    def getInvoiceAddress():
        """Returns the invoice address.
        """

    def getShippingAddress():
        """Returns the shipping address.
        """
        
    def hasAddresses():
        """Returns True if context has at least one address.
        """
        
################################################################################
# Customers        
################################################################################

class ICustomersContainer(Interface):
    """A marker interface for customer folder content objects.
    """

class ICustomer(Interface):
    """A customer can buy products from the shop.
    """
    
class ICustomerManagement(Interface):
    """Provides methods to manage customer content objects.
    """
    def getAuthenticatedCustomer():
       """Returns the current authenticated customer.
       """

    def getCustomerById(id):
        """Returns a customer by given id
        """    

    def getCustomers():
       """
       """

    def hasCustomer(customer):
       """
       """        