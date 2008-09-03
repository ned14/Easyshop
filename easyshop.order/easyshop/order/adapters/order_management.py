# Zope imports
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

# zope imports
from zope.interface import implements
from zope.component import adapts

# CMF imports
from Products.CMFCore.utils import getToolByName

# EasyShop import
from easyshop.core.interfaces import IItemManagement 
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICopyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxes

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()

class OrderManagement(object):
    """An adapter, which provides order management for shop content objects.
    """
    implements(IOrderManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.orders = context.orders

    def addOrder(self, customer=None, cart=None):
        """
        """
        cartmanager = ICartManagement(self.context)
        if customer is None:
            cm = ICustomerManagement(self.context)
            customer = cm.getAuthenticatedCustomer()

        if cart is None:
            cart = cartmanager.getCart()

        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        ## The current user may not be allowed to create an order, so we
        ## temporarily change the security context to use a temporary
        ## user with manager role.
        old_sm = getSecurityManager()
        tmp_user = UnrestrictedUser(
            old_sm.getUser().getId(),
            '', ['Manager'], 
            ''
        )
        
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)
  
        # Add a new order
        new_id = self._createOrderId()
        self.orders.invokeFactory("Order", id=new_id)
        new_order = getattr(self.orders, new_id)
        
        # Add cart items to order
        IItemManagement(new_order).addItemsFromCart(cart)

        # Add total tax 
        new_order.setTax(ITaxes(cart).getTaxForCustomer())
        
        # Add shipping values to order
        sm = IShippingPriceManagement(self.context)
        new_order.setShippingPriceNet(sm.getPriceNet())
        new_order.setShippingPriceGross(sm.getPriceGross())
        new_order.setShippingTax(sm.getTaxForCustomer())
        new_order.setShippingTaxRate(sm.getTaxRateForCustomer())

        # Add payment price values to order 
        pp = IPaymentPriceManagement(self.context)
        new_order.setPaymentPriceGross(pp.getPriceGross())
        new_order.setPaymentPriceNet(pp.getPriceNet())
        new_order.setPaymentTax(pp.getTaxForCustomer())
        new_order.setPaymentTaxRate(pp.getTaxRateForCustomer())
        
        # Copy Customer to Order
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        cm = ICopyManagement(customer)
        cm.copyTo(new_order)
                    
        ## Reset security manager
        setSecurityManager(old_sm)
        
        # Index with customer again
        new_order.reindexObject()
        
        return new_order

    def deleteOrder(self, id):
        """
        """
        self.orders.manage_delObjects([id])

    def getOrderByUID(self, uid):
        """
        """
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        lazy_cat = uid_catalog(UID=uid)
        o = lazy_cat[0].getObject()
        return o
                
    def getOrders(self, filter=None, sorting="created", sort_order="reverse"):
        """
        """
        catalog = getToolByName(self.orders, "portal_catalog")
        path = "/".join(self.orders.getPhysicalPath())
        
        query = {
            "path" : path,
            "portal_type" : "Order",
            "sort_on"     : sorting,
            "sort_order"  : sort_order,
        }
                
        if filter is not None:
            query["review_state"] = filter
                        
        brains = catalog.searchResults(query)
        return [brain.getObject() for brain in brains]

    def getOrdersForAuthenticatedCustomer(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        orders = []
        for order in self.getOrders():
            if order.getCustomer().getId() == customer.getId():
                orders.append(order)

        return orders

    def getOrdersForCustomer(self, customer_id):
        """
        """
        orders = []
        for order in self.getOrders():
            if order.getCustomer().getId() == customer_id:
                orders.append(order)

        return orders
        
    def _createOrderId(self):
        """Creates a new unique order id.
        """
        from DateTime import DateTime;
        now = DateTime()

        return str(now.millis())