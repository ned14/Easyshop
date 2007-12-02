# Zope imports 
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import IOrderClosed
from easyshop.core.interfaces import IOrderPayed
from easyshop.core.interfaces import IOrderSent
from easyshop.core.interfaces import IOrderSubmitted
        
class OrderClosed(object):
    """
    """
    implements(IOrderClosed)
    
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
        
class OrderSubmitted(object):
    """
    """
    implements(IOrderSubmitted)
    
    def __init__(self, context):
        self.context = context