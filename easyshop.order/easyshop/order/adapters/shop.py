# Zope imports
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.event import notify

# CMF imports
from Products.CMFCore.utils import getToolByName

# EasyShop import
from Products.EasyShop.interfaces import IItemManagement 
from Products.EasyShop.interfaces import IOrderManagement
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IShippingManagement
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IPaymentPrices
from Products.EasyShop.interfaces import IShop
from Products.EasyShop.events import OrderSubmitted

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id."""
    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()

class OrderManagement:
    """An adapter, which provides order management for shop content objects.
    """
    implements(IOrderManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.orders = context.orders

    def addOrder(self, customer=None, cart=None, notify_=True):
        """Adds a new order on base of the current customer and current cart.        
           It should be called after the payment process is completed.
        """
        shop = self.context.getShop()
        cartmanager = ICartManagement(self.context)
        if customer is None:
            customer = ICustomerManagement(shop).getAuthenticatedCustomer()

        if cart is None:
            cart = cartmanager.getCart()
  
        # Add a new order
        new_id = self.createOrderId()
        self.orders.invokeFactory("Order", id=new_id)
        new_order = getattr(self.orders, new_id)

        # Add shipping values to order
        sm = IShippingManagement(shop)
        new_order.setShippingPriceNet(sm.getPriceNet())
        new_order.setShippingPriceGross(sm.getPriceGross())
        new_order.setShippingTax(sm.getTaxForCustomer())
        new_order.setShippingTaxRate(sm.getTaxRateForCustomer())

        # Add cart items to order
        IItemManagement(new_order).addItemsFromCart(cart)

        # Add payment price values to order 
        pp = IPaymentPrices(shop)
        new_order.setPaymentPriceGross(pp.getPriceGross())
        new_order.setPaymentPriceNet(pp.getPriceNet())
        new_order.setPaymentTax(pp.getTaxForCustomer())
        new_order.setPaymentTaxRate(pp.getTaxRateForCustomer())
        
        # Copy the customer object to the order 
        self.copyCustomerToOrder(customer, new_order)
        
        # Delete cart
        cartmanager.deleteCart(cart.getId())

        # Index with customer again
        new_order.reindexObject()
        
        # Fire up event
        if notify_ == True:
            notify(OrderSubmitted(new_order))
                    
        return new_order

    def copyCustomerToOrder(self, customer, order):
        """
        """
        ## The current user may not be allowed to copy and paste so we
        ## temporarily change the security context to use a temporary
        ## 'Manager' user.
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        old_sm = getSecurityManager()
        tmp_user = UnrestrictedUser(
            old_sm.getUser().getId(),
            '', ['Manager'], 
            ''
        )
        
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)

        # Copy Customer to Order         
        data = self.context.customers.manage_copyObjects(ids=[customer.getId()])
        order.manage_pasteObjects(data)        

        ## Reset security manager
        setSecurityManager(old_sm)
        
    def getOrders(self, filter=None, sorting="created", sort_order="reverse"):
        """Returns orders filtered by given filter.
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
        """Returns all orders for the actual customer.
        """
        # get authenticated customer        
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()

        orders = []
        for order in self.getOrders():
            if order.getCustomer().getId() == customer.getId():
                orders.append(order)

        return orders

    def createOrderId(self):
        """Creates a new unique order id
        """
        from DateTime import DateTime;
        now = DateTime()

        return str(now.millis())
        
    def getOrderByUID(self, uid):
        """Returns order by given uid.        
        """
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        lazy_cat = uid_catalog(UID=uid)
        o = lazy_cat[0].getObject()
        return o