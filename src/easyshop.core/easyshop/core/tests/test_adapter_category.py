# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement

class TestCategoryCategoryManagement(EasyShopTestCase):
    """
    """
    def testGetTopLevelCategories(self):
        """
        """
        cm = ICategoryManagement(self.portal.myshop.categories.category_1)
        category_ids = [c.id for c in cm.getTopLevelCategories()]
        
        self.failUnless(len(category_ids) == 2)
        for id in ["category_11", "category_12"]:
            self.failUnless(id in category_ids)

        cm = ICategoryManagement(self.category_2)
        self.failUnless(len(cm.getCategories()) == 0)
        
    def testGetCategories(self):
        """
        """
        cm = ICategoryManagement(self.portal.myshop.categories.category_1)
        category_ids = [c.id for c in cm.getCategories()]
        
        for id in ["category_11", "category_12", "category_111"]:
            self.failUnless(id in category_ids)
        
        cm = ICategoryManagement(self.portal.myshop.categories.category_1.category_11)
        category_ids = [c.id for c in cm.getCategories()]
        self.assertEqual(["category_111"], category_ids)

        cm = ICategoryManagement(self.portal.myshop.categories.category_2)
        self.failUnless(len(cm.getCategories()) == 0)
         

class TestCategoryProductManagement(EasyShopTestCase):
    """
    """
    def testGetProducts(self):
        """
        """
        pm = IProductManagement(self.portal.myshop.categories.category_1)
        self.assertEqual(pm.getProducts(), [])

        pm = IProductManagement(self.portal.myshop.categories.category_2)
        self.assertEqual(pm.getProducts(), [])

        pm = IProductManagement(self.portal.myshop.categories.category_1.category_11)
        product_ids = [p.getId() for p in pm.getProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])
                
    def testGetAllProducts(self):
        """
        """
        pm = IProductManagement(self.portal.myshop.categories.category_1)
        product_ids = [p.getId() for p in pm.getAllProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])

        pm = IProductManagement(self.portal.myshop.categories.category_1.category_11)
        product_ids = [p.getId() for p in pm.getAllProducts()]
        self.assertEqual(product_ids, ["product_1", "product_2"])
        
    def testGetAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.portal.myshop.categories.category_1)
        self.assertEqual(pm.getAmountOfProducts(), 0)

        pm = IProductManagement(self.portal.myshop.categories.category_2)
        self.assertEqual(pm.getAmountOfProducts(), 0)

        pm = IProductManagement(self.portal.myshop.categories.category_1.category_11)
        self.assertEqual(pm.getAmountOfProducts(), 2)
        
    def testGetTotalAmountOfProducts(self):
        """
        """
        pm = IProductManagement(self.portal.myshop.categories.category_1)
        self.assertEqual(pm.getTotalAmountOfProducts(), 2)

        pm = IProductManagement(self.portal.myshop.categories.category_2)
        self.assertEqual(pm.getTotalAmountOfProducts(), 0)

        pm = IProductManagement(self.portal.myshop.categories.category_1.category_11)
        self.assertEqual(pm.getTotalAmountOfProducts(), 2)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCategoryCategoryManagement))
    suite.addTest(makeSuite(TestCategoryProductManagement))    
    
    return suite
                                               