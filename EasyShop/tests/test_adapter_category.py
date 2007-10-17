# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ICategoryManagement
from Products.EasyShop.interfaces import IProductManagement

class TestCategoryCategoryManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)                

    def testHasCategories(self):
        """
        """
        cm = ICategoryManagement(self.category_1)
        self.assertEqual(cm.hasCategories(), True)

        cm = ICategoryManagement(self.category_2)
        self.assertEqual(cm.hasCategories(), False)
        
    def testHasParentCategory(self):
        """
        """
        cm = ICategoryManagement(self.category_1)
        self.assertEqual(cm.hasParentCategory(), False)

        cm = ICategoryManagement(self.category_1.category_11)
        self.assertEqual(cm.hasParentCategory(), True)
                
    def testGetCategories(self):
        """
        """
        cm = ICategoryManagement(self.category_1)
        category_ids = [c.getId() for c in cm.getCategories()]
        self.assertEqual(["category_11", "category_12"], category_ids)

        cm = ICategoryManagement(self.category_2)
        self.assertEqual(cm.getCategories(), [])
        
    def testGetTotalCategories(self):
        """
        """
        cm = ICategoryManagement(self.category_1)
        category_ids = [c.getId() for c in cm.getTotalCategories()]
        self.assertEqual(["category_11", "category_111", "category_12"], category_ids)

        cm = ICategoryManagement(self.category_1.category_11)
        category_ids = [c.getId() for c in cm.getTotalCategories()]
        self.assertEqual(["category_111"], category_ids)

        cm = ICategoryManagement(self.category_2)
        self.assertEqual([], cm.getTotalCategories())
         
    def testGetTopLevelCategories(self):
        """
        """
        cm = ICategoryManagement(self.category_1)
        category_ids = [c.getId for c in cm.getTopLevelCategories()]
        self.assertEqual(["category_11", "category_12"], category_ids)

        cm = ICategoryManagement(self.category_1.category_11)
        category_ids = [c.getId for c in cm.getTopLevelCategories()]
        self.assertEqual(["category_111"], category_ids)

        cm = ICategoryManagement(self.category_2)
        category_ids = [c.getId for c in cm.getTopLevelCategories()]        
        self.assertEqual([], category_ids)


class TestCategoryProductManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)                

    def testGetProducts(self):
        """
        """
        pm = IProductManagement(self.category_1)
        self.assertEqual(pm.getProducts(), [])

        pm = IProductManagement(self.category_2)
        self.assertEqual(pm.getProducts(), [])

        pm = IProductManagement(self.category_1.category_11)
        product_ids = [p.getId() for p in pm.getProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])
                
    def testGetAllProducts(self):
        """
        """
        pm = IProductManagement(self.category_1)
        product_ids = [p.getId() for p in pm.getAllProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])

        pm = IProductManagement(self.category_1.category_11)
        product_ids = [p.getId() for p in pm.getAllProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])
        
    def testGetAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.category_1)
        self.assertEqual(pm.getAmountOfProducts(), 0)

        pm = IProductManagement(self.category_2)
        self.assertEqual(pm.getAmountOfProducts(), 0)

        pm = IProductManagement(self.category_1.category_11)
        self.assertEqual(pm.getAmountOfProducts(), 2)
        
    def testGetTotalAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.category_1)
        self.assertEqual(pm.getTotalAmountOfProducts(), 2)

        pm = IProductManagement(self.category_2)
        self.assertEqual(pm.getTotalAmountOfProducts(), 0)

        pm = IProductManagement(self.category_1.category_11)
        self.assertEqual(pm.getTotalAmountOfProducts(), 2)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCategoryCategoryManagement))
    suite.addTest(makeSuite(TestCategoryProductManagement))    
    
    return suite
                                               