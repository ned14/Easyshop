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
        title        = 'easyshop.order',
        description  = 'Orders for EasyShop',
        path         = 'profiles/default',
        product      = 'easyshop.order',
        profile_type = EXTENSION,
        for_         = IPloneSiteRoot)    
