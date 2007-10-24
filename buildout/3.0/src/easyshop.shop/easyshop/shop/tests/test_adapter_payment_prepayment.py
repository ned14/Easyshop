# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType

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
                                               