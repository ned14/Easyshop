# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class IOrder(Interface):
    """An marker interface for order content objects.
    """
    
class IOrderManagement(Interface):
    """Provides methods to manage order content objects.
    """
    def addOrder(customer=None, cart=None):
        """Adds a new order on base of the current customer and current cart.
        """

    def deleteOrder(id):
        """Deletes order with given id.
        """

    def getOrderByUID(uid):
        """Returns order by given uid.        
        """

    def getOrders(filter=None):
        """Returns orders filtered by given filter.
        """

    def getOrdersForAuthenticatedCustomer():
        """Returns all orders for the current customer
        """

    def getOrdersForCustomer(customer_id):
        """Returns orders for customer with given id.
        """
        
class IOrderItem(Interface):
    """Marker interface to mark order item content objects.
    """
                    
class IOrdersContainer(Interface):
    """An marker interface for containers which hold orders.
    """
    
class IOrderSubmitted(Interface):
    """An event fired when an order has been submitted.
    """    
    context = Attribute("The order that has been submitted")
    
class IOrderPayed(Interface):
    """An event fired when an order has been payed.
    """    
    context = Attribute("The order that has been payed")
    
class IOrderSent(Interface):
    """An event fired when an order has been sent
    """    
    context = Attribute("The order that has been sent")
    
class IOrderClosed(Interface):
    """An event fired when an order has been closed
    """    
    context = Attribute("The order that has been closed")