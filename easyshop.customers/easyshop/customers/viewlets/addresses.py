# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop Products
from easyshop.core.config import _
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IAddressManagement

class AddressesViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('addresses.pt')
    
    def getAddresses(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        
        am = IAddressManagement(customer)
        return am.getAddresses()    
