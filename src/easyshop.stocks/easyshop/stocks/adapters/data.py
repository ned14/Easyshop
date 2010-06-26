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
        delivery_min  = self.context.getDeliveryTimeMin()
        delivery_max  = self.context.getDeliveryTimeMax()
        time_unit     = self.context.getDeliveryTimeUnit()

        if delivery_min == delivery_max:

            if delivery_min == "1":
                time_unit = time_unit[:-1]
                
            time_period = delivery_min
            
        else:            
            time_period = "%s-%s" % (delivery_min, delivery_max)
            
        return {
            "available"   : self.context.getAvailable(),
            "time_period" : time_period,
            "time_unit"   : time_unit,
            "url"         : self.context.absolute_url()
        }