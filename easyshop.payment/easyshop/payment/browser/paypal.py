# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import IOrderManagement

class PayPalView(BrowserView):
    """
    """
    def receivePayment(self):
        """
        """
        shop = self.context
        
        # Get cart - Note: self.request.get("order") doesn't work!
        order_uid = self.request.get("QUERY_STRING")[6:]
        order = IOrderManagement(shop).getOrderByUID(order_uid)
        
        # change order state to "payed_not_sent"
        wftool = getToolByName(self, "portal_workflow")
        wftool.doActionFor(order, "pay_not_sent")