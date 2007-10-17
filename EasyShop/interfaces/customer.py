# zope imports
from zope.interface import Interface

class ICustomerContent(Interface):
    """Marker interface for customer content objects.
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