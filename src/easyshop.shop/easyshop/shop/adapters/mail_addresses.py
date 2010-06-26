# zope imports
from zope.component import adapts  
from zope.component import getUtility
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.interfaces import ISiteRoot

# easyshop imports
from easyshop.core.interfaces import IMailAddresses
from easyshop.core.interfaces import IShop

class ShopMailAddresses(object):
    """An adapter which provides IMailAddresses for shop content objects.
    """
    implements(IMailAddresses)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def getSender(self):
        """Returns sender from shop content object. If it is blank returns Plone
        default sender. If it is also blank returns None.
        """
        name = self.context.getMailFromName()
        if name == "":
            name = getUtility(ISiteRoot).email_from_name

        address = self.context.getMailFromAddress()   
        if address == "":
            address = getUtility(ISiteRoot).email_from_address

        if address == "":
            return None

        if name != "":
            return "%s <%s>" % (name, address)
        else:
            return address
        
    def getReceivers(self):
        """Returns receivers from shop content object. If they are blank 
        returns Plone default receiver. If it is also blank returns None.
        """
        receivers = self.context.getMailTo()
        if len(receivers) == 0:
            sender = self.getSender()
            if sender is None:
                return ()
            else:
                return (sender,)
        else:
            return receivers