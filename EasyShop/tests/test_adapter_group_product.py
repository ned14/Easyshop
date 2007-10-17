# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IProductManagement

class TestGroupProductManager(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testGetProducts_1(self):
        """As manager
        """
        pm = IProductManagement(self.group_1)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, ["product_1", "product_2"])

        pm = IProductManagement(self.group_2)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, ["product_1"])

    def testGetProducts_2(self):
        """As anonymous. Note hat only products return for which the user has
        the View permission.
        """
        self.logout()
        
        pm = IProductManagement(self.group_1)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, [])

        pm = IProductManagement(self.group_2)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, [])

    def testGetProducts_3(self):
        """As anonymous, with product_2 published.
        """
        wftool = getToolByName(self.shop, "portal_workflow")
        wftool.doActionFor(self.product_2, "publish")
        
        self.logout()
        
        pm = IProductManagement(self.group_1)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, ["product_2"])

        pm = IProductManagement(self.group_2)
        product_ids = [p.getId() for p in pm.getProducts()]        
        self.assertEqual(product_ids, [])


    def testGetAmountOfProducts_1(self):
        """As manager
        """
        pm = IProductManagement(self.group_1)
        self.assertEqual(len(pm.getProducts()), 2)

        pm = IProductManagement(self.group_2)
        self.assertEqual(len(pm.getProducts()), 1)

    def testGetAmountOfProducts_2(self):
        """As anonymous. Note that only products are counted for which the user
        has the View permission.
        """
        self.logout()
        pm = IProductManagement(self.group_1)
        self.assertEqual(len(pm.getProducts()), 0)

        pm = IProductManagement(self.group_2)
        self.assertEqual(len(pm.getProducts()), 0)
        
    def testGetAmountOfProducts_3(self):
        """As anonymous, with product_2 published.
        """
        wftool = getToolByName(self.shop, "portal_workflow")
        wftool.doActionFor(self.product_2, "publish")
        
        self.logout()

        pm = IProductManagement(self.group_1)
        self.assertEqual(len(pm.getProducts()), 1)

        pm = IProductManagement(self.group_2)
        self.assertEqual(len(pm.getProducts()), 0)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGroupProductManager))
    return suite                                               