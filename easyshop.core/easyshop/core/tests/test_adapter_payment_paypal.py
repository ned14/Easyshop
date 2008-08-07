# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IType

class TestPayPalType(EasyShopTestCase):
    """
    """
    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods["paypal"]    
        self.assertEqual(IType(cod).getType(), "paypal")

class TestPayPalCompleteness(EasyShopTestCase):
    """
    """
    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods["paypal"]
        self.assertEqual(ICompleteness(cod).isComplete(), True)

class TestPayPalPaymentProcessor(EasyShopTestCase):
    """
    """
    def testProcess(self):
        """
        """
        # Todo: find a way to test paypal

class TestPayPalValidity(EasyShopTestCase):
    """
    """
    def testValidity(self):
        """
        """
        self.shop.setPayPalId("")
        paypal = self.shop.paymentmethods.paypal
        result = IValidity(paypal).isValid()        
        self.failUnless(result == False)
        
        self.shop.setPayPalId("john@doe.com")
        result = IValidity(paypal).isValid()
        self.failUnless(result == True)        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPayPalType))
    suite.addTest(makeSuite(TestPayPalCompleteness))        
    suite.addTest(makeSuite(TestPayPalValidity))
    
    return suite
                                               