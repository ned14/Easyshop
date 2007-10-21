# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IOrderManagement

class IMyOrdersView(Interface):    
    """
    """
    def getOrders():
        """Returns the orders for the authenticated customer as dict.
        """
       
class MyOrdersView(BrowserView):
    """
    """
    implements(IMyOrdersView)
    
    def getOrders(self):
        """
        """
        om = IOrderManagement(self.context)
        orders = om.getOrdersForAuthenticatedCustomer()
        
        result = []
        for order in orders:
            # Todo: Get rid of this
            order_view = getMultiAdapter((order, self.request), name="order")
                                    
            temp = {
                "id" : order.getId(),
                "url": order.absolute_url(),
                "price_gross" : order_view.getPriceForCustomer(),
                "shipping" : order_view.getShipping(),
                "payment"  : order_view.getPaymentValues(),
                "items_" : order_view.getItems(),                      # items is a python key word.
            }
            result.append(temp)

        return result
        