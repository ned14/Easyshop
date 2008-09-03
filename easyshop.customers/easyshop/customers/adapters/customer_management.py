# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import safe_unicode

# easyshop imports
from easyshop.customers.content import Customer
from easyshop.core.interfaces import ICopyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ISessionManagement
from easyshop.core.interfaces import IShop

class CustomerManagement(object):
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
            customer = Customer(id=id)
            self.customers._setObject(id, customer)
            return True
        else:
            return False

    def getAuthenticatedCustomer(self):
        """Returns the customer or a session customer for anonymous user. If it
        doesn't already exist, creates a new one.
        """        
        mtool = getToolByName(self.context, "portal_membership")
        mid = mtool.getAuthenticatedMember().getId()

        sm = getUtility(ISessionManagement)
        sid = sm.getSID(self.context.REQUEST)
        
        if mid is None:
            if base_hasattr(self.sessions, sid) == False:
                customer = Customer(id=sid)
                self.sessions._setObject(sid, customer)
                
            customer = self.sessions[sid]
        else:
            if base_hasattr(self.sessions, sid) == True:
                self.transformCustomer(mid, sid)
            
            if base_hasattr(self.customers, mid) == False:
                customer = Customer(id=mid)
                self.customers._setObject(mid, customer)
                
                # Set customers info
                customer = self.customers[mid]
                self._setCustomerInfo(customer)
                    
            customer = self.customers[mid]        

        # Update roles and mappings
        wftool = getToolByName(self.context, "portal_workflow")
        wftool.notifyCreated(customer)

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
    
    def transformCustomer(self, mid, sid):
        """
        """
        # Not logged in
        if mid is None:
            return False

        # There is already a personalized customer    
        if base_hasattr(self.customers, mid) == True:
            return False

        # There is no session customer            
        if base_hasattr(self.sessions, sid) == False:
            return False

        session_customer = self.sessions[sid]
        ICopyManagement(session_customer).copyTo(self.customers, mid)
        
        # Set customer info
        customer = self.customers[mid]
        self._setCustomerInfo(customer)
        
        self.sessions.manage_delObjects([sid])

        return True
        
    def _setCustomerInfo(self, customer):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        member = mtool.getMemberById(customer.id)
        if member is not None:
            customer.email = safe_unicode(member.getProperty("email"))