# zope imports
from zope.viewlet.viewlet import ViewletBase

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import IAddressManagement

class AddressesViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('addresses.pt')
    
    def getAddresses(self):
        """
        """
        am = IAddressManagement(self.context)
        return am.getAddresses()    
