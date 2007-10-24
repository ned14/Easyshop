# zope imports
from zope.interface import Interface

class IShippingManagement(Interface):
    """
    """    
    def getSelectedShippingMethod():
        """Returns the selected shipping method of the current authenticated 
        customer.
        """
            
    def getPriceNet():
        """Returns the net price of shipping.
        """

    def getPriceGross():
        """Returns the gross price of shipping. Returns the first valid        
        (All criteria are True) shipping price.
        """

    def getPriceForCustomer():
        """Returns the gross price of shipping for actual customer
        """

    def getShippingPrice(id):
        """Returns shipping price by given id
        """

    def getShippingPrices():
        """Returns all shipping prices
        """

    def getShippingMethod(id):
        """Returns shipping method by given id.
        """    
        
    def getShippingMethods():
        """Returns all shipping methods.
        """
        
    def getTaxRate():
        """Returns tax rate for shipping by means of tax manager
        """

    def getTaxRateForCustomer():
        """Returns tax for shipping for actual customer by means of tax
           manager
        """

    def getTax():
        """Returns absolute tax for shipping by means of tax manager
        """

    def getTaxForCustomer():
        """Returns absolute tax for shipping for actual customer by means of
           tax manager
        """

class IShippingPrice(Interface):
    """A price for shipping.
    """

class IShippingMethod(Interface):
    """A shipping method.
    """
    
class IShippingPricesContainer(Interface):
    """A container to hold shipping prices
    """

class IShippingMethodsContainer(Interface):
    """A container to hold shipping methods
    """    