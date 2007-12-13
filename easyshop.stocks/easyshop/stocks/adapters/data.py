# zope imports
from zope.component import adapts
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IStockInformation

class StockInformationData:
    """
    """
    implements(IData)
    adapts(IStockInformation)

    def __init__(self, context):
        """
        """
        self.context = context

    def asDict(self):
        """
        """
        time_period = "%s-%s %s" % (self.context.getDeliveryTimeMin(), 
                                    self.context.getDeliveryTimeMax(), 
                                    self.context.getDeliveryTimeUnit())
        return {
            "available"   : self.context.getAvailable(),
            "time_period" : time_period,
        }