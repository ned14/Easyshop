# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ICustomer

class TestCustomerManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCustomerManagement, self).afterSetUp()
        self.cm = ICustomerManagement(self.shop)

    def testAddCustomers(self):
        """
        """
        result = self.cm.addCustomer("c1")
        self.failIf(result == False)
        
        result = self.cm.addCustomer("c2")
        self.failIf(result == False)
        
        result = self.cm.addCustomer("c3")
        self.failIf(result == False)
        
        result = self.cm.addCustomer("c4")
        self.failIf(result == False)
        
        ids = [c.getId for c in self.cm.getCustomers()]
        self.assertEqual(ids, ["c1", "c2", "c3", "c4"])
                
    def testGetAuthenticatedCustomer_1(self):
        """As anonymous, returns standard customer
        """
        self.logout()
        customer = self.cm.getAuthenticatedCustomer()
        self.assertEqual(customer.getId(), "DUMMY_SESSION")

    def testGetAuthenticatedCustomer_2(self):
        """As member
        """
        self.login("newmember")
        customer = self.cm.getAuthenticatedCustomer()

        self.failUnless(ICustomer.providedBy(customer))
        self.assertEqual(customer.getId(), "newmember")
        
    def testGetCustomerById_1(self):
        """Existing customer
        """
        result = self.cm.addCustomer("c1")
        self.failIf(result == False)
        
        customer = self.cm.getCustomerById("c1")

        self.assertEqual(customer.getId(), "c1")
        self.failUnless(ICustomer.providedBy(customer))

    def testGetCustomerById_2(self):
        """Non-existing customer
        """
        customer = self.cm.getCustomerById("doe")
        self.assertEqual(customer, None)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerManagement))
    return suite
                                               