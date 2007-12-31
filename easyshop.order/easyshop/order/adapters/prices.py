# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrder

class OrderPrices:
    """Adapter which provides IPrices for order content objects.
    """
    implements(IPrices)
    adapts(IOrder)
    
    def __init__(self, context):
        """
        """
        self.context = context        
        self.item_management = IItemManagement(context)

    def getPriceNet(self):
        """Returns the total net price of the order.
        """
        total = 0.0

        for item in self.item_management.getItems():
            total += item.getPriceNet()
            total -= item.getDiscountNet()

        total += self.context.getPaymentPriceNet()
        total += self.context.getShippingPriceNet()

        return total

    def getPriceGross(self):
        """Returns the total gross price of the order.
        """
        total = 0.0        
        for item in self.item_management.getItems():
            total += item.getPriceGross()
            total -= item.getDiscountGross()

        total += self.context.getPaymentPriceGross()
        total += self.context.getShippingPriceGross()

        return total

    def getPriceForCustomer(self):
        """In the context of an order PriceGross and PriceForCustomer are 
           equal.
        """
        return self.getPriceGross()
