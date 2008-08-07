# Suppress DeprecationWarnings, we really don't want any in these tests
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)
from transaction import commit

from AccessControl.SecurityManagement import newSecurityManager

from Testing import ZopeTestCase

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# PloneTestCase imports
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite

# Five imports
from Products.Five.testbrowser import Browser as BaseBrowser
from Products.Five import zcml

import easyshop.core

PloneTestCase.setupPloneSite(
    products=["easyshop.core",
              "easyshop.shop",
              "easyshop.catalog",
              "easyshop.carts",
              "easyshop.criteria",
              "easyshop.customers",
              "easyshop.discounts",
              "easyshop.groups",
              "easyshop.information",
              "easyshop.kss",
              "easyshop.login",
              "easyshop.management",
              "easyshop.order",
              "easyshop.payment",
              "easyshop.shipping",
              "easyshop.stocks",
              "easyshop.taxes",
             ])


# easyshop imports
from easyshop.core.tests import utils

class Browser(BaseBrowser):
    """
    """
    def addAuthorizationHeader(self, user=PloneTestCase.default_user, password=PloneTestCase.default_password):
        """ add an authorization header using the given or default credentials """
        self.addHeader('Authorization', 'Basic %s:%s' % (user, password))
        return self
    
    def dc(self, filename="/Users/Kai/Downloads/test-output.html"):
        open(filename, 'w').write(self.contents)
            
class EasyShopLayer(PloneSite):
    """
    """
    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        ZopeTestCase.installPackage("easyshop.core")
        ZopeTestCase.installPackage("easyshop.shop")
        ZopeTestCase.installPackage("easyshop.catalog")
        ZopeTestCase.installPackage("easyshop.carts")
        ZopeTestCase.installPackage("easyshop.criteria")
        ZopeTestCase.installPackage("easyshop.customers")
        ZopeTestCase.installPackage("easyshop.discounts")
        ZopeTestCase.installPackage("easyshop.groups")
        ZopeTestCase.installPackage("easyshop.information")
        ZopeTestCase.installPackage("easyshop.kss")
        ZopeTestCase.installPackage("easyshop.login")
        ZopeTestCase.installPackage("easyshop.management")
        ZopeTestCase.installPackage("easyshop.order")
        ZopeTestCase.installPackage("easyshop.payment")
        ZopeTestCase.installPackage("easyshop.shipping")
        ZopeTestCase.installPackage("easyshop.stocks")
        ZopeTestCase.installPackage("easyshop.taxes")
        
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.core:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.shop:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.catalog:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.carts:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.criteria:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.customers:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.discounts:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.groups:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.information:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.kss:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.login:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.management:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.order:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.payment:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.shipping:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.stocks:default')
        setup_tool.runAllImportStepsFromProfile('profile-easyshop.taxes:default')

        # login as admin (copied from `loginAsPortalOwner`)
        uf = app.acl_users
        user = uf.getUserById(PloneTestCase.portal_owner).__of__(uf)
        newSecurityManager(None, user)

        utils.createTestEnvironment(portal)
        
        commit()
        ZopeTestCase.close(app)

    @classmethod
    def tearDown(cls):
        pass
        
class EasyShopMixin(object):
    """
    """
    def afterSetUp(self):
        """
        """
        self.setRoles(("Manager",))
        self.shop       = self.portal.myshop
        self.category_1 = self.portal.category_1
        self.category_2 = self.portal.category_2
        self.product_1  = self.portal.product_1
        self.product_2  = self.portal.product_2
        self.group_1    = self.portal.group_1
        self.group_2    = self.portal.group_2

class EasyShopFunctionalMixin(EasyShopMixin):
    """
    """
    def afterSetUp(self):
        """
        """
        super(EasyShopFunctionalMixin, self).afterSetUp()

        # let users join themselves
        self.portal.manage_permission('Add portal member', roles=["Anonymous", "Manager"], acquire=0)        
        
        # let users select their own password        
        self.portal.manage_changeProperties(validate_email=False)    

        workflow = self.portal.portal_workflow
        workflow.doActionFor(self.portal.myshop, 'publish')
        workflow.doActionFor(self.portal.myshop.products.product_1, 'publish')
        workflow.doActionFor(self.portal.myshop.products.product_2, 'publish')
        workflow.doActionFor(self.portal.myshop.products.product_42, 'publish')
        
class EasyShopTestCase(EasyShopMixin, PloneTestCase.PloneTestCase):
    """Base class for integration tests for the 'iqpp.rating' product.
    """
    layer = EasyShopLayer
  
class EasyShopFunctionalTestCase(EasyShopFunctionalMixin, PloneTestCase.FunctionalTestCase):
    """Base class for functional integration tests for the 'iqpp.rating' product.
    """
    layer = EasyShopLayer