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
from Products.EasyShop.interfaces import IAddressManagement

class IOrdersView(Interface):
    """
    """
    def getOrders():
        """Returns orders of the shop. Dependent on given filter. As dict.
        """    
        
class OrdersView(BrowserView):
    """
    """
    implements(IOrdersView)

    def getOrders(self):
        """
        """
        tool = getToolByName(self.context, 'translation_service')
                
        shop = self.context.getShop()
                
        wftool = getToolByName(self.context, "portal_workflow")
        filter = self.request.get("filter", "all")        
        if filter == "all": filter = None

        sorting = self.request.get("sorting", "created")
        order   = self.request.get("order", "descending")

        orders = []
        om = IOrderManagement(shop)
        
        for order in om.getOrders(filter, sorting, order):
            
            # get fullname
            fullname = "There is no customer."
            customer = order.getCustomer()
            if customer is not None:
                am = IAddressManagement(customer)        
                address = am.getInvoiceAddress()
                if address is not None:
                    fullname = address.getName(reverse=True)
                
                
            # created
            created = tool.ulocalized_time(order.created(), long_format=True)
            
            orders.append({
                "id"            : order.getId(),
                "url"           : order.absolute_url(),
                "created"       : created,
                "customer_name" : fullname,
                "review_state"  : wftool.getInfoFor(order, "review_state")
            })
            
        return orders