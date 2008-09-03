# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class ICart(Interface):
    """A cart of a shop. Can hold serveral cart items.
    """
    id = Attribute(
        "The unique id of the card. Either the member id or the session id")

class ICartsContainer(Interface):
    """A container which hold carts.
    """

class ICartManagement(Interface):
    """Provides methods to manage cart content objects
    """
    def createCart():
        """Creates a cart for the current user.
        """
        
    def deleteCart(id):
        """Deletes a cart
        """
        
    def getCart():
        """Returns the cart of actual session / authenticated member. Returns
        None if there isn't one.
        """

    def getCarts(sorted_on="date", sort_order="descending"):
        """Returns carts depending of given paramenters.
        """
        
    def getCartById(id):
        """Returns a cart by given id.
        """
        
    def hasCart(id):
        """Returns True if the current user has a cart.
        """
        
class ICartsContainer(Interface):
    """A marker interface for carts folder content objects.
    """

class ICartItem(Interface):
    """A cart item holds a selected product and its amount an properties.
    """
    amount     = Attribute("The selected amount of the product")
    product    = Attribute("The selected product.")
    properties = Attribute("The selected attributes of the product")