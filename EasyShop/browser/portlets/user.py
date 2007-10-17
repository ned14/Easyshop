# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement

class IPortletUserView(Interface):    
    """
    """
    def getMyAccountUrl():
        """Returns URL to "my account".
        """
    
    def getUserName():
        """Returns fullname or member_id
        """

    def isAnonymous():
        """Returns True if actual member is anonymous
        """
        
class PortletUserView(BrowserView):
    """
    """
    implements(IPortletUserView)

    def getMyAccountUrl(self):
        """
        """
        return "%s/my-account" % self.context.getShop().absolute_url()
        
    def getUserName(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")        
        m = mtool.getAuthenticatedMember()
        
        if m.getProperty("firstname") and m.getProperty("lastname"):
            return m.getProperty("firstname") + " " + m.getProperty("lastname")
        else:    
            return m.getId()

    def isAnonymous(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        return mtool.isAnonymousUser()
