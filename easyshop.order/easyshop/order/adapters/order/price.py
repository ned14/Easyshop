# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrder

class OrderPriceCalculator:
    """Provides IPrices for order content objects.
    """
    implements(IPrices)
    adapts(IOrder)
    
    def __init__(self, context):
        """
        """
        self.context = context        
        self.item_management = IItemManagement(context)

    def getPriceNet(self):
        """Returns the total net price of the order, which means the sum
           of all items plus shipping price
        """
        total = 0.0

        for item in self.item_management.getItems():
            total += item.getPriceNet()

        total += self.context.getPaymentPriceNet()
        total += self.context.getShippingPriceNet()

        return total

    def getPriceGross(self):
        """Returns the total gross price of the order, which means the sum
           of all items plus shipping price
        """
        total = 0.0        
        for item in self.item_management.getItems():
            total += item.getPriceGross()

        total += self.context.getPaymentPriceGross()
        total += self.context.getShippingPriceGross()

        return total

    def getPriceForCustomer(self):
        """In the context of an order PriceGross and PriceForCustomer are 
           equal.
        """
        return self.getPriceGross()
