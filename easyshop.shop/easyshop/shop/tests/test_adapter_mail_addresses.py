# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.app.controlpanel.mail import IMailSchema

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IMailAddresses

class TestShopMailAddresses(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestShopMailAddresses, self).afterSetUp()
        self.addresses = IMailAddresses(self.shop)

    def testGetAddresses1(self):
        """No information entered.
        """        
        sender = self.addresses.getSender()
        self.assertEqual(sender, None)
        
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ())

        
    def testGetAddresses2(self):
        """Information entered in portal. Note: Portal has just one email 
        address which is used for sender and receiver.
        """
        utool = getToolByName(self.shop, "portal_url")
        portal = utool.getPortalObject()
                
        mail = IMailSchema(portal)
        
        # Just address is entered
        mail.set_email_from_address("john@doe.com")
        
        sender = self.addresses.getSender()
        self.assertEqual(sender, "Site Administrator <john@doe.com>")

        # receiver is same as sender
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("Site Administrator <john@doe.com>",))
        
        # Address and name is entered
        mail.set_email_from_name("John Doe")
        
        sender = self.addresses.getSender()
        self.assertEqual(sender, "John Doe <john@doe.com>")

        # receiver is same as sender
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("John Doe <john@doe.com>",))
        
    def testGetAddresses3(self):
        """Information entered in shop.
        """
        self.shop.setMailFromAddress("john@doe.com")
        
        sender = self.addresses.getSender()
        self.assertEqual(sender, "Site Administrator <john@doe.com>")
        
        # Just sender is set, hence receiver is same as sender
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("Site Administrator <john@doe.com>",))
        
        # Name and address is set
        self.shop.setMailFromName("John Doe")
        
        sender = self.addresses.getSender()
        self.assertEqual(sender, "John Doe <john@doe.com>")

        # Just sender is set, hence receiver is same as sender
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("John Doe <john@doe.com>",))

        # Receivers set
        self.shop.setMailTo(["Jane Doe <jane@doe.com>"])

        sender = self.addresses.getSender()
        self.assertEqual(sender, "John Doe <john@doe.com>")
        
        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("Jane Doe <jane@doe.com>",))

        # More receivers set
        self.shop.setMailTo(["Jane Doe <jane@doe.com>", "baby@joe.com"])

        receivers = self.addresses.getReceivers()
        self.assertEqual(receivers, ("Jane Doe <jane@doe.com>", "baby@joe.com"))
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopMailAddresses))
    return suite