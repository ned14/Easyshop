# CMFCore imports
from Products.CMFCore import DirectoryView

# CMFPlone imports
from Products.CMFPlone.interfaces import IPloneSiteRoot

# GenericSetup imports
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    DirectoryView.registerDirectory('skins', globals())
    
    # register profile
    profile_registry.registerProfile(
        name         = 'default',
        title        = 'EasyShopSkins',
        description  = 'Skinsfolder for EasyShop for Plone 2.5',
        path         = 'profiles/default',
        product      = 'EasyShopSkins',
        profile_type = EXTENSION,
        for_         = IPloneSiteRoot)