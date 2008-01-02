# CMFCore imports
from Products.CMFCore import DirectoryView

# CMFPlone imports
from Products.CMFPlone.interfaces import IPloneSiteRoot

# GenericSetup imports
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    
    # register profile
    profile_registry.registerProfile(
        name         = 'default',
        title        = 'easyshop.login',
        description  = 'Login for EasyShop',
        path         = 'profiles/default',
        product      = 'easyshop.login',
        profile_type = EXTENSION,
        for_         = IPloneSiteRoot)    
