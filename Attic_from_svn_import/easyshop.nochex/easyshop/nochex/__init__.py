# GenericSetup imports
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

# CMFPlone imports
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes

from easyshop.core.config import *

def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    import easyshop.nochex.content

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # register profile
    profile_registry.registerProfile(
        name         = 'default',
        title        = 'easyshop.nochex',
        description  = 'Nochex payment processing for EasyShop',
        path         = 'profiles/default',
        product      = 'easyshop.nochex',
        profile_type = EXTENSION,
        for_         = IPloneSiteRoot)                                  
