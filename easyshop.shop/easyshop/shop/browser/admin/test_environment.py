# Python imports
import random
import os 

# Zope imports
from Globals import package_home

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *

LETTERS = [chr(i) for i in range(65, 91)]

class TestEnvironmentView(BrowserView):
    """
    """
    def createProducts1(self):
        """
        """                            
        shop = self.context

        categories = []
        for i in range(1, 21):
            id = "category-%s" % i
            shop.categories.manage_addProduct["easyshop.shop"].addCategory(id, title="Category %s" %i)
            
            category = shop.categories.get(id)
            categories.append(category)
            
            wftool = getToolByName(self.context, "portal_workflow")
            wftool.doActionFor(category, "publish")

        for i in range(1, 101):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct["easyshop.shop"].addProduct(id, title=title)
            product = shop.products.get(id)            

            # add category
            category = random.choice(categories)
            category.addReference(product, "category_products")
            
            wftool.doActionFor(product, "publish")
            
        self.context.portal_catalog.manage_catalogRebuild()
        
    def createProducts2(self):
        """Add all products to one category.
        """                            
        shop = self.context
                
        id = "category"
        shop.categories.manage_addProduct["easyshop.shop"].addCategory(id, title="Category")        
        category = shop.categories.get(id)
        
        wftool = getToolByName(self.context, "portal_workflow")
        wftool.doActionFor(category, "publish")

        for i in range(1, 21):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct["easyshop.shop"].addProduct(id, title=title)
            product = shop.products.get(id)

            img = os.path.join(package_home(globals()), '../../tests/test_2.jpg')
            img = open(img)
        
            product.setImage(img)

            category.addReference(product, "category_products")            
            wftool.doActionFor(product, "publish")
            
        self.context.portal_catalog.manage_catalogRebuild()
        
    def createTitle(self):
        """
        """
        return "".join([random.choice(LETTERS) for i in range(1, 10)])