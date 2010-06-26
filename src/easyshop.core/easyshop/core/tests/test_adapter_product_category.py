# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICategoryManagement

class TestProductCategoryManager(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestProductCategoryManager, self).afterSetUp()
        self.shop.products.invokeFactory(
            "Product", 
            id="product_3", 
            price=19.0)        
            
        self.product_3 = self.shop.products.product_3
        
    def testGetTopLevelCategories_1(self):
        """
        """
        cm = ICategoryManagement(self.product_1)

        ids = [c.getId() for c in cm.getTopLevelCategories()]        
        self.assertEqual(ids, ["category_11"])

        # adding some more
        self.shop.categories.invokeFactory("Category", id="category_a")
        self.shop.categories.invokeFactory("Category", id="category_b")
        
        self.shop.categories.category_a.addReference(
            self.product_1, 
            "categories_products")
        self.shop.categories.category_b.addReference(
            self.product_1, 
            "categories_products")
                                        
        ids = [c.getId() for c in cm.getTopLevelCategories()]
        
        self.failUnless(len(ids) == 3)
        for id in ["category_11", "category_a", "category_b"]:
            self.failUnless(id in ids)

    def testGetTopLevelCategories_2(self):
        """No categories there
        """
        cm = ICategoryManagement(self.product_3)
        self.assertEqual(cm.getTopLevelCategories(), [])

                                        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductCategoryManager))
    return suite
                                               