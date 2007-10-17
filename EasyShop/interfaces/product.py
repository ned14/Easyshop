from zope.interface import Interface

class IProductContent(Interface):
    """Marker interface to mark product content objects.
    """

class IProductManagement(Interface):
    """Provides methods to handle product content objects.
    """
    
    def getAllProducts():
        """Returns all products (top and sub levels).
        """
        
    def getAmountOfProducts():
        """Returns the amount products.
        """        

    def getProducts():
        """Returns top level products.
        """

    def getTotalAmountOfProducts():
        """Returns the amount of products of all subcategories.
        """
        
class IProductSelectorContent(Interface):
    """A marker interface for product selector content objects.
    """