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

class TestPrepaymentType(EasyShopTestCase):
    """
    """
    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods["prepayment"]    
        self.assertEqual(IType(cod).getType(), "simple-payment")

class TestPrepaymentCompleteness(EasyShopTestCase):
    """
    """
    def testIsComplete(self):
        """
        """
        cod = self.shop.paymentmethods["prepayment"]                
        self.assertEqual(ICompleteness(cod).isComplete(), True)

class TestPrepaymentPaymentProcessor(EasyShopTestCase):
    """
    """
    def testProcess(self):
        """
        """
        cod = self.shop.paymentmethods["prepayment"]                
        self.assertEqual(IPaymentProcessing(cod).process(), "NOT_PAYED")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPrepaymentType))
    suite.addTest(makeSuite(TestPrepaymentCompleteness))        
    suite.addTest(makeSuite(TestPrepaymentPaymentProcessor))        
    return suite
                                               