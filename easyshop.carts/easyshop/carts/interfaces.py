# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class ICart(Interface):
    """Marker interface to mark cart content objects.
    """
    id = Attribute(
        "The unique id of the card. Either the member id or the session id")
    
class ICartItem(Interface):
    """Marker interface to mark cart item content objects.
    """

class ICartManagement(Interface):
    """Provides methods to manage cart content objects
    """
    def addCart(id):
       """Adds a cart
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
        
    def getCartByUID(uid):        
        """Returns a cart by given uid.
        """

    def hasCart(id):
        """Returns True if the current user has a cart.
        """