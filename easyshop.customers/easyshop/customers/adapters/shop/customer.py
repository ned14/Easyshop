# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone.utils import base_hasattr

# easyshop imports
from easyshop.customers.content import Customer
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop

class CustomerManagement:
    """Provides customer management for shop content objects.
    """
    implements(ICustomerManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.customers = self.context.customers
        self.sessions  = self.context.sessions

    def addCustomer(self, id):
        """
        """
        if base_hasattr(self.customers, id) == False:
            customer = Customer(id=id, title=id)
            self.customers._setObject(id, customer)
            return True
        else:
            return False

    # TODO: Rename it to getCustomer        
    def getAuthenticatedCustomer(self):
        """Returns the customer or a session customer for anonymous user.

           If it doesn't already exist, creates a new one
        """
        mtool = getToolByName(self.context, "portal_membership")
        mid = mtool.getAuthenticatedMember().getId()
        
        if mid is None:
            try:
                sid = self.context.REQUEST.SESSION.getId()
            except AttributeError:
                sid = "DUMMY_SESSION"
            
            if base_hasattr(self.sessions, sid) == False:
                customer = Customer(id=sid)
                self.sessions._setObject(sid, customer)
            customer = self.sessions[sid]    
        else:
            if base_hasattr(self.customers, mid) == False:
                customer = Customer(mid)
                self.customers._setObject(mid, customer)

            customer = self.customers[mid]        
            
        return customer

    def getCustomerById(self, id):
        """Returns a customer by given id
        """
        try:
            return self.customers[id]
        except KeyError:
            return None

    def getCustomers(self):
        """Returns all customers as brains.
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.customers.getPhysicalPath()),
            portal_type = "Customer",
        )
        
        return brains