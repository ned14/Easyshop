# zope imports
from zope.interface import implements

# iqpp imports
from easyshop.core.interfaces import IStockAmountIsZeroEvent

class StockAmountIsZeroEvent(object):
    """
    """
    implements(IStockAmountIsZeroEvent)
    
    def __init__(self, product):
        """
        """
        self.product = product