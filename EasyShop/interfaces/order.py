# zope imports
from zope.interface import Interface

class IOrder(Interface):
    """Marker interface to mark order content objects.
    """
    
class IOrderManagement(Interface):
    """Provides methods to manage order content objects.
    """
    def addOrder(customer=None, cart=None):
        """Adds a new order.        
        """

    def copyCustomerToOrder(customer, order):
        """copys customer to order.
        """

    def getOrders(filter=None):
        """Returns orders filtered by given filter.
        """

    def getOrdersForAuthenticatedCustomer():
        """Returns all orders for the actual customer
        """

    def createOrderId():
        """Creates a new unique order id
        """

    def getOrderByUID(uid):
        """Returns order by given uid.        
        """