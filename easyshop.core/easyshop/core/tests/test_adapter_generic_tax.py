# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IValidity

class TestValidityManager(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestValidityManager, self).afterSetUp()                
        self.shop.taxes.invokeFactory("DefaultTax", id="default_tax")
        self.default_tax = self.shop.taxes.default_tax

    def testIsValid_1(self):
        """Without criteria
        """
        v = IValidity(self.default_tax)
        self.assertEqual(v.isValid(self.product_1), True)

    def testIsValid_2(self):
        """With one invalid criterion.
        """
        self.default_tax.invokeFactory("DateCriteria", id="date_criterion")
        start = end = DateTime() + 1
        self.default_tax.date_criterion.setStart(start)
        self.default_tax.date_criterion.setEnd(end)
        
        v = IValidity(self.default_tax)
        self.assertEqual(v.isValid(self.product_1), False)
    
    def testIsValid_3(self):
        """With one valid criterion.
        """
        self.default_tax.invokeFactory("DateCriteria", id="date_criterion")
        start = DateTime() - 1
        end   = DateTime() + 1
        self.default_tax.date_criterion.setStart(start)
        self.default_tax.date_criterion.setEnd(end)
        
        v = IValidity(self.default_tax)
        self.assertEqual(v.isValid(self.product_1), True)
        
    def testIsValid_4(self):
        """With one invalid and one valid criterion.
        """
        # invalid
        self.default_tax.invokeFactory("DateCriteria", id="date_criterion")    
        start = end = DateTime() + 1
        self.default_tax.date_criterion.setStart(start)
        self.default_tax.date_criterion.setEnd(end)
        
        # valid (product_1 is in group_1; see utils.createTestEnvironment)
        self.default_tax.invokeFactory("GroupCriteria", id="group_criterion")
        self.default_tax.group_criterion.setGroups(["group_1"])        
        v = IValidity(self.default_tax)
        self.assertEqual(v.isValid(self.product_1), False)

    def testIsValid_5(self):
        """With two valid criteria.
        """
        # valid
        self.default_tax.invokeFactory("DateCriteria", id="date_criterion")    
        start = DateTime() - 1
        end   = DateTime() + 1
        self.default_tax.date_criterion.setStart(start)
        self.default_tax.date_criterion.setEnd(end)
        
        # valid (product_1 is in group_1; see utils.createTestEnvironment)
        self.default_tax.invokeFactory("GroupCriteria", id="group_criterion")
        self.default_tax.group_criterion.setGroups(["group_1"])
        v = IValidity(self.default_tax)
        self.assertEqual(v.isValid(self.product_1), True)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityManager))
    return suite
                                               