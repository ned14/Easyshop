# zope imports
from zope.interface import implements

# iqpp imports
from iqpp.easyshop.interfaces import IStockAmountIsZeroEvent

class StockAmountIsZeroEvent(object):
    """
    """
    implements(IStockAmountIsZeroEvent)
    
    def __init__(self, product):
        """
        """
        self.product = product