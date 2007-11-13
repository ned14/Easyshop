# Zope imports
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone.utils import base_hasattr

# easyshop imports
from easyshop.customers.content import Customer
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ISessionManagement
from easyshop.core.interfaces import IShop

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id."""
    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


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
        import pdb; pdb.set_trace()        
        data = self.sessions.manage_cutObjects(ids=[sid])
        self.customers.manage_pasteObjects(data)
        
        self.customers.manage_renameObjects((sid,), (mid,))

        ## Reset security manager
        setSecurityManager(old_sm)

        return True