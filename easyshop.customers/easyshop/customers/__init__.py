# CMFPlone imports
from Products.CMFPlone.interfaces import IPloneSiteRoot

# GenericSetup imports
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """    
    # register profile
    profile_registry.registerProfile(
        name         = 'default',
        title        = 'easyshop.customers',
        description  = 'Customers for EasyShop',
        path         = 'profiles/default',
        product      = 'easyshop.customers',
        profile_type = EXTENSION,
        for_         = IPloneSiteRoot)    