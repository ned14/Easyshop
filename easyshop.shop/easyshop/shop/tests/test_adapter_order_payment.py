# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPaymentManagement

class TestOrderPaymentManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestOrderPaymentManagement, self).afterSetUp()                        
        
        self.shop.orders.invokeFactory("Order", "order")
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
        self.order.invokeFactory("Customer", "test")
        pm = IPaymentManagement(self.order)
        m = pm.getSelectedPaymentMethod()
        
        self.assertEqual(m.getId(), "prepayment")
            
    def testProcessSelectedPaymentMethod(self):
        """
        """
        self.order.invokeFactory("Customer", "test")
        pm = IPaymentManagement(self.order)
        result = pm.processSelectedPaymentMethod()

        self.assertEqual(result, "NOT_PAYED")

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderPaymentManagement))
    return suite
                                               