# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IImageManagement

class TestFormatterInfos(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestFormatterInfos, self).afterSetUp()
        self.fi_1 = IFormats(self.shop)
        self.fi_2 = IFormats(self.shop.categories.category_1)

    # TODO: test for setFormats
    # TODO: test for effective formats
    def testGetFormats(self):
        """
        """
        fi_1 = self.fi_1.getFormats()
        fi_2 = self.fi_2.getFormats()
            
        self.assertEqual(fi_1["lines_per_page"], 1)
        self.assertEqual(fi_1["products_per_line"], 2)
        self.assertEqual(fi_1["image_size"], "mini")
        self.assertEqual(fi_1["text"], "short_text")
        self.assertEqual(fi_1["product_height"], 0)

        self.assertEqual(fi_2["lines_per_page"], 1)
        self.assertEqual(fi_2["products_per_line"], 2)
        self.assertEqual(fi_2["image_size"], "mini")
        self.assertEqual(fi_2["text"], "short_text")
        self.assertEqual(fi_2["product_height"], 0)
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFormatterInfos))
    return suite
                                               