# zope imports
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShopManagement

class MyOrdersView(BrowserView):
    """
    """
    def getOrders(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        om = IOrderManagement(shop)
        orders = om.getOrdersForAuthenticatedCustomer()
        wftool = getToolByName(self.context, "portal_workflow")
        ttool  = getToolByName(self.context, 'translation_service')
        
        result = []
        for order in orders:
            # TODO: Get rid of using order view
            order_view = getMultiAdapter((order, self.request), name="order")
            created = ttool.ulocalized_time(order.created(), long_format=True)
            temp = {
                "id"            : order.getId(),
                "url"           : order.absolute_url(),
                "price_gross"   : order_view.getPriceForCustomer(),
                "shipping"      : order_view.getShipping(),
                "payment"       : order_view.getPaymentValues(),
                "items_"        : order_view.getItems(),
                "creation_date" : created,
                "state"         : wftool.getInfoFor(order, "review_state"),
                "tax"           : order_view.getTax(),
            }
            result.append(temp)

        return result