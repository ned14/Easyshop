# Zope imports 
from zope.interface import implements

# easyshop imports
from iqpp.easyshop.interfaces import IOrderClosed
from iqpp.easyshop.interfaces import IOrderPayed
from iqpp.easyshop.interfaces import IOrderSent
from iqpp.easyshop.interfaces import IOrderSubmitted
        
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