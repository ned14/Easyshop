# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IShippingMethodManagement

class TestShippingMethodManagement(EasyShopTestCase):
    """
    """
    def testGetSelectedShippingMethod(self):
        """
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getSelectedShippingMethod()
        
        self.assertEqual(result.getId(), "standard")
        
    def testGetShippingMethod_1(self):
        """Requested shipping method exists.
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getShippingMethod("standard")        

        self.assertEqual(result.getId(), "standard")

    def testGetShippingMethod_2(self):
        """Requested shipping method doesn't exist.
        """
        sm = IShippingMethodManagement(self.shop)
        result = sm.getShippingMethod("dummy")

        self.failUnless(result is None)
        
    def testGetShippingMethods(self):
        """
        """
        sm = IShippingMethodManagement(self.shop)
        methods = sm.getShippingMethods()
        ids = [method.getId() for method in methods]

        self.assertEqual(ids, ["standard"])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShippingMethodManagement))
    return suite