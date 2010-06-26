# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from iqpp.easyshop.tests import utils
from iqpp.easyshop.interfaces import ICompleteness
from iqpp.easyshop.interfaces import IPaymentProcessing
from iqpp.easyshop.interfaces import IType

class TestPrepaymentType(EasyShopTestCase):
    """
    """
    def testGetType(self):
        """
        """
        cod = self.shop.paymentmethods["prepayment"]    
        self.assertEqual(IType(cod).getType(), "generic-payment")

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
        pm = self.shop.paymentmethods["prepayment"]                
        result = IPaymentProcessing(pm).process()        
        self.assertEqual(result.code, "NOT_PAYED")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPrepaymentType))
    suite.addTest(makeSuite(TestPrepaymentCompleteness))        
    suite.addTest(makeSuite(TestPrepaymentPaymentProcessor))        
    return suite
                                               