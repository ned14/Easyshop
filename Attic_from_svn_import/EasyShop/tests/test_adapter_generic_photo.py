# Python imports
import os

# Zope imports
from DateTime import DateTime
from Globals import package_home

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from Products.EasyShop.config import *
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IPhotoManagement

class TestPhotoManagement_1(EasyShopTestCase):
    """Test with no photos.
    """
    def afterSetUp(self):
        """
        """
        super(TestPhotoManagement_1, self).afterSetUp()
        self.logout()
        
    def testGetMainPhoto(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.getMainPhoto(), None)
        
    def testGetPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.getPhotos(), [])
                        
    def testHasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.hasPhotos(), False)

class TestPhotoManagement_2(EasyShopTestCase):
    """Test with photos as own objects within the folderish product.
    """
    def afterSetUp(self):
        """
        """
        super(TestPhotoManagement_2, self).afterSetUp()
        self.product_1.invokeFactory("Photo", id="photo_1")
        self.product_1.invokeFactory("Photo", id="photo_2")        
        self.logout()
        
    def testGetMainPhoto(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.getMainPhoto().getId(), "photo_1")
        
    def testGetPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        ids = [p.getId() for p in pm.getPhotos()]
        
        self.assertEqual(ids, ["photo_1", "photo_2"])
                        
    def testHasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.hasPhotos(), True)

class TestPhotoManagement_3(EasyShopTestCase):
    """Test with photo as attribute.
    """
    def afterSetUp(self):
        """
        """
        super(TestPhotoManagement_3, self).afterSetUp()                        
                
        img = os.path.join(package_home(product_globals), 'tests/test.jpg')
        img = open(img)
        
        self.product_1.setImage(img)
        self.logout()
        
    def testGetMainPhoto(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.getMainPhoto().getId(), "product_1")
        
    def testGetPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        ids = [p.getId() for p in pm.getPhotos()]
        
        self.assertEqual(ids, ["product_1"])
                        
    def testHasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.hasPhotos(), True)

class TestPhotoManagement_4(EasyShopTestCase):
    """Test with photos as attribute and objects.
    """
    def afterSetUp(self):
        """
        """
        super(TestPhotoManagement_4, self).afterSetUp()                    
                
        img = os.path.join(package_home(product_globals), 'tests/test.jpg')
        img = open(img)
        
        self.product_1.setImage(img)
        self.product_1.invokeFactory("Photo", id="photo_1")
        self.product_1.invokeFactory("Photo", id="photo_2")
                                
        self.logout()
        
    def testGetMainPhoto(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.getMainPhoto().getId(), "product_1")
        
    def testGetPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        ids = [p.getId() for p in pm.getPhotos()]
        
        self.assertEqual(ids, ["product_1", "photo_1", "photo_2"])
                        
    def testHasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.product_1)
        self.assertEqual(pm.hasPhotos(), True)
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPhotoManagement_1))
    suite.addTest(makeSuite(TestPhotoManagement_2))
    suite.addTest(makeSuite(TestPhotoManagement_3))    
    suite.addTest(makeSuite(TestPhotoManagement_4))        
    return suite
                                               