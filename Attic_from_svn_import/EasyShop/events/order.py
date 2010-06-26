# Zope imports 
from zope.interface import implements
from zope.interface import Interface
from zope.interface import Attribute

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


class OrderSubmitted(object):
    """
    """
    implements(IOrderSubmitted)
    
    def __init__(self, context):
        self.context = context
            
class OrderPayed(object):
    """
    """
    implements(IOrderPayed)
    
    def __init__(self, context):
        self.context = context
        
class OrderSent(object):
    """
    """
    implements(IOrderSent)
    
    def __init__(self, context):
        self.context = context
        
class OrderClosed(object):
    """
    """
    implements(IOrderClosed)
    
    def __init__(self, context):
        self.context = context