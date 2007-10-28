# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFPlone imports
from Products.CMFPlone import PloneMessageFactory as _

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IAddressManagement

class IManageAddressBookView(Interface):    
    """
    """
    def deleteAddress():
        """
        """             
    
    def getCustomer(self):
        """Returns authenticated customer.
        """
        
    def getAddresses():
        """Returns addresses of authenticated customer.
        """
       
class ManageAddressBookView(BrowserView):
    """
    """
    implements(IManageAddressBookView)

    def deleteAddress(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
                
        # delete address
        toDeleteAddressId = self.context.request.get("id")
        am = IAddressManagement(customer)
        am.deleteAddress(toDeleteAddressId)
        
        # add message
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(_("The address has been deleted."))
                                        
        # redirect to addressbook
        url = "%s/manage-addressbook" % self.context.absolute_url()
        self.context.request.response.redirect(url)
            
    def getCustomer(self):
        """
        """
        cm = ICustomerManagement(self.context)
        return cm.getAuthenticatedCustomer()
                
    def getAddresses(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        return am.getAddresses()
    