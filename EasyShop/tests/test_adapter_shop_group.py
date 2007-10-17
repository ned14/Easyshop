# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IGroupManagement

class TestShopGroupManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testGetGroups(self):
        """
        """
        gm = IGroupManagement(self.shop)
        ids = [g.getId() for g in gm.getGroups()]
        
        self.assertEqual(ids, ["group_1", "group_2"])
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopGroupManagement))
    return suite
                                               