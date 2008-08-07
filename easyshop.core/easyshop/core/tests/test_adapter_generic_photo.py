# Python imports
import os

# Zope imports
from DateTime import DateTime
from Globals import package_home

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from easyshop.core.config import *
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IImageManagement

class TestImageManagement_1(EasyShopTestCase):
    """Test with no images.
    """
    def afterSetUp(self):
        """
        """
        super(TestImageManagement_1, self).afterSetUp()
        self.logout()
        
    def testGetMainImage(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.getMainImage(), None)
        
    def testGetImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.getImages(), [])
                        
    def testHasImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.hasImages(), False)

class TestImageManagement_2(EasyShopTestCase):
    """Test with images as own objects within the folderish product.
    """
    def afterSetUp(self):
        """
        """
        super(TestImageManagement_2, self).afterSetUp()
        self.product_1.invokeFactory("EasyShopImage", id="image_1")
        self.product_1.invokeFactory("EasyShopImage", id="image_2")        
        self.logout()
        
    def testGetMainImage(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.getMainImage().getId(), "image_1")
        
    def testGetImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        ids = [p.getId() for p in pm.getImages()]
        
        self.assertEqual(ids, ["image_1", "image_2"])
                        
    def testHasImage(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.hasImages(), True)

class TestImageManagement_3(EasyShopTestCase):
    """Test with image as attribute.
    """
    def afterSetUp(self):
        """
        """
        super(TestImageManagement_3, self).afterSetUp()                        
                
        img = os.path.join(package_home(globals()), 'test.jpg')
        img = open(img)
        
        self.product_1.setImage(img)
        self.logout()
        
    def testGetMainImage(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.getMainImage().getId(), "product_1")
        
    def testGetImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        ids = [p.getId() for p in pm.getImages()]
        
        self.assertEqual(ids, ["product_1"])
                        
    def testHasImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.hasImages(), True)

class TestImageManagement_4(EasyShopTestCase):
    """Test with images as attribute and objects.
    """
    def afterSetUp(self):
        """
        """
        super(TestImageManagement_4, self).afterSetUp()                    
                
        img = os.path.join(package_home(globals()), 'test.jpg')
        img = open(img)
        
        self.product_1.setImage(img)
        self.product_1.invokeFactory("EasyShopImage", id="image_1")
        self.product_1.invokeFactory("EasyShopImage", id="image_2")
                                
        self.logout()
        
    def testGetMainImage(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.getMainImage().getId(), "product_1")
        
    def testGetImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        ids = [p.getId() for p in pm.getImages()]
        
        self.assertEqual(ids, ["product_1", "image_1", "image_2"])
                        
    def testHasImages(self):
        """
        """
        pm = IImageManagement(self.product_1)
        self.assertEqual(pm.hasImages(), True)
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestImageManagement_1))
    suite.addTest(makeSuite(TestImageManagement_2))
    suite.addTest(makeSuite(TestImageManagement_3))    
    suite.addTest(makeSuite(TestImageManagement_4))        
    return suite
                                               