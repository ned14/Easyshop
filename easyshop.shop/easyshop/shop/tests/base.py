# Suppress DeprecationWarnings, we really don't want any in these tests
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)
from transaction import commit

from AccessControl.SecurityManagement import newSecurityManager

from Testing import ZopeTestCase

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite

from Products.Five.testbrowser import Browser as BaseBrowser

PloneTestCase.setupPloneSite(
    products=["easyshop.shop",])

# easyshop imports
from easyshop.shop.tests import utils

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
        
        ZopeTestCase.installPackage("easyshop.catalog")
        ZopeTestCase.installPackage("easyshop.checkout")
        ZopeTestCase.installPackage("easyshop.login")
        ZopeTestCase.installPackage("easyshop.shop")

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