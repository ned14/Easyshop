# zope imports
from zope.interface import Interface

class IPropertyContent(Interface):
    """A marker interface for a property content objects.
    """
    
class IPropertyManagement(Interface):
    """Provides methods to manage property content objects.
    """    
    def getPriceForCustomer(property_id, option_name):
        """Returns the customer price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """
       
    def getPriceGross(property_id, option_name):
        """Returns the gross price of a context's property with given id and
        option name.
        """

    def getPriceNet(property_id, option_name):
        """Returns the net price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """

    def getProperties():
        """Returns all properties.
        """
        
    def getProperty(id):
        """Returns the property with given title.
        
        Using title, because then a property could be deleted and added
        again. This wouldn't work with id or uid.
        
        This requires, that title per property is unique. This will be done in
        edit view.
        """