# Suppress DeprecationWarnings, we really don't want any in these tests
from warnings import simplefilter
simplefilter('ignore', DeprecationWarning)

from Testing import ZopeTestCase
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

ZopeTestCase.installProduct('EasyShop')
ZopeTestCase.installProduct('easyshop.carts')
ZopeTestCase.installProduct('easyshop.taxes')
setupPloneSite(products=['EasyShop', "easyshop.carts", 'easyshop.taxes'])

class EasyShopTestCase(PloneTestCase):
  """Base class for integration tests for the 'iqpp.rating' product.
  """

class EasyShopFunctionalTestCase(FunctionalTestCase):
  """Base class for functional integration tests for the 'iqpp.rating' product.
  """
  