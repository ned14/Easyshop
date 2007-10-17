# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IOrderManagement
from Products.EasyShop.interfaces import IPaymentManagement

class TestOrderPaymentManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)
        
        self.shop.orders.invokeFactory("EasyShopOrder", "order")
        self.order = self.shop.orders.order
                        
    def testDeletePaymentMethod(self):
        """
        """            
        om = IPaymentManagement(self.order)
        self.assertRaises(Exception, om.deletePaymentMethod)
        
    def testGetPaymentMethods(self):
        """
        """
        om = IPaymentManagement(self.order)
        self.assertRaises(Exception, om.deletePaymentMethod)

    def testGetSelectedPaymentMethod(self):
        """
        """
        self.order.manage_addProduct["EasyShop"].addEasyShopCustomer("test")
        pm = IPaymentManagement(self.order)
        m = pm.getSelectedPaymentMethod()
        
        self.assertEqual(m.getId(), "prepayment")
            
    def testProcessSelectedPaymentMethod(self):
        """
        """
        self.order.manage_addProduct["EasyShop"].addEasyShopCustomer("test")
        pm = IPaymentManagement(self.order)
        result = pm.processSelectedPaymentMethod()

        self.assertEqual(result, "NOT_PAYED")

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderPaymentManagement))
    return suite
                                               