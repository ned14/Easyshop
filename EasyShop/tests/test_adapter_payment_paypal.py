# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ICompleteness
from Products.EasyShop.interfaces import IPaymentProcessing
from Products.EasyShop.interfaces import IType

class TestPayPalType(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods["paypal"]    
        self.assertEqual(IType(cod).getType(), "paypal")

class TestPayPalCompleteness(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods["paypal"]
        self.assertEqual(ICompleteness(cod).isComplete(), True)

class TestPayPalPaymentProcessor(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testProcess(self):
        """
        """
        # Todo: find a way to test paypal
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPayPalType))
    suite.addTest(makeSuite(TestPayPalCompleteness))        
    return suite
                                               