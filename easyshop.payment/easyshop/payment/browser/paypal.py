# Zope imports
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IOrderManagement

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
        
        # We need a new security manager here, because this transaction should 
        # usually just be allowed by a Manager except here.
        old_sm = getSecurityManager()
        tmp_user = UnrestrictedUser(
            old_sm.getUser().getId(),
            '', ['Manager'], 
            ''
        )

        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)
        
        wftool.doActionFor(order, "pay_not_sent")
        
        ## Reset security manager
        setSecurityManager(old_sm)
        