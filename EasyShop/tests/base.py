# Suppress DeprecationWarnings, we really don't want any in these tests
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)

from transaction import commit

from AccessControl.SecurityManagement import newSecurityManager

from Testing import ZopeTestCase

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite

from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

ZopeTestCase.installProduct('EasyShop')
PloneTestCase.setupPloneSite(
    products=["EasyShop",
              "easyshop.carts",
              "easyshop.catalog",              
              "easyshop.criteria",
              "easyshop.customer",
              "easyshop.order",              
              "easyshop.payment",              
              "easyshop.shipping",
              "easyshop.taxes",
              ])

# EasyShop imports
from Products.EasyShop.tests import utils

class EasyShopLayer(PloneSite):
    """
    """
    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        portal = app.plone

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
        
class EasyShopMixin:
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
                
class EasyShopTestCase(EasyShopMixin, PloneTestCase.PloneTestCase):
    """Base class for integration tests for the 'iqpp.rating' product.
    """
    layer = EasyShopLayer
  
class EasyShopFunctionalTestCase(FunctionalTestCase):
  """Base class for functional integration tests for the 'iqpp.rating' product.
  """
  