# zope imports
from zope.interface import Interface

class ITaxes(Interface):
    """
    """
    def getTax():
       """Returns default tax for a product
       """

    def getTaxForCustomer():
       """Returns tax for a customer
       """

    def getTaxRate():
       """Returns default tax for a product
       """

    def getTaxRateForCustomer():
       """Returns tax for a customer
       """

class ITax(Interface):
    """A marker interface to mark tax content objects.
    """
    
class ITaxManagement(Interface):
    """Provides methods to manage tax content objects.
    """
    def getCustomerTaxes():
        """Returns all customer taxes.
        """
        
    def getDefaultTaxes():
        """Returns all default taxes.
        """

    def getTax(id):
        """Returns tax object by given id.
        """
                
class ITaxesContainer(Interface):
    """A container which holds tax content objects.
    """
