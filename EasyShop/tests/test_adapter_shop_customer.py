# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import ICustomerContent

class TestCustomerManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCustomerManagement, self).afterSetUp()
        self.cm = ICustomerManagement(self.shop)
        
        self.shop.customers.invokeFactory("EasyShopCustomer", "c1")
        self.shop.customers.invokeFactory("EasyShopCustomer", "c2")
        self.shop.customers.invokeFactory("EasyShopCustomer", "c3")
        self.shop.customers.invokeFactory("EasyShopCustomer", "c4")
        
    def testGetAuthenticatedCustomer_1(self):
        """As anonymous, returns standard customer
        """
        self.logout()
        customer = self.cm.getAuthenticatedCustomer()
        self.assertEqual(customer.getId(), "standard-customer")

    def testGetAuthenticatedCustomer_2(self):
        """As member
        """
        self.login("newmember")
        customer = self.cm.getAuthenticatedCustomer()

        self.failUnless(ICustomerContent.providedBy(customer))
        self.assertEqual(customer.getId(), "newmember")
        
    def testGetCustomers(self):
        """
        """
        ids = [c.getId() for c in self.cm.getCustomers()]
        self.assertEqual(ids, ["c1", "c2", "c3", "c4"])
        
    def testGetCustomerById_1(self):
        """Existing customer
        """
        customer = self.cm.getCustomerById("c1")

        self.assertEqual(customer.getId(), "c1")
        self.failUnless(ICustomerContent.providedBy(customer))

    def testGetCustomerById_2(self):
        """Non-existing customer
        """
        customer = self.cm.getCustomerById("doe")
        self.assertEqual(customer, None)
        
    def testHasCustomer(self):
        """
        """
        result = self.cm.hasCustomer("c1")
        self.assertEqual(result, True)

        result = self.cm.hasCustomer("doe")
        self.assertEqual(result, False)

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerManagement))
    return suite
                                               