# zope imports
from zope.interface import Interface

class IItemManagement(Interface):
    """Provides methods to manage item content objects.
    """
    def addItem(product, amount=1):
        """Adds a item.
        """

    def addItemsFromCart(cart):
        """At the items from another Cart.
        """

    def deleteItemByOrd(ord):
        """Deletes the item by passed ord.
        """

    def deleteItem(id):
        """Deletes item with passed id.
        """

    def getItem(id):
        """Returns item with passed id.
        """

    def getItems():
        """Returns all items.
        """

    def hasItems():
        """Returns True if there is at least one item.
        """