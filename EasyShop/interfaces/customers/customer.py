# zope imports
from zope.interface import Interface

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