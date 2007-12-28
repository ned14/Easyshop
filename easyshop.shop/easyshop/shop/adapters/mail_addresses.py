# zope imports
from zope.component import adapts  
from zope.interface import implements

# plone imports
from plone.app.controlpanel.mail import IMailSchema

# easyshop imports
from easyshop.core.interfaces import IMailAddresses
from easyshop.core.interfaces import IShop

class ShopMailAddresses(object):
    """An adapter which provides IMailAddresses for shop content objects.
    """
    implements(IMailAddresses)
    adapts(IShop)
    
    def getSender(self):
        """
        """
        name = self.context.getMailFromName()
        if name == "":
            address = IMailSchema(self.context).email_from_name

        address = self.context.getMailFromAddress()   
        if address == "":
            address = IMailSchema(self.context).email_from_address

        if address == "":
            raise "No Email Address"
            
        if name != "":
            return "%s <%s>" % (name, address)
        else:
            return address
        
    def getReceivers(self):
        """
        """
        receivers = ", ".join(self.context.getMailTo())
        if len(receivers) == 0:
            return (self.getSender(),)
        else:
            return receivers