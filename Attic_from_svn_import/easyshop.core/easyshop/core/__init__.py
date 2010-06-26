from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes

from easyshop.core.config import *

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    from AccessControl import allow_module
    allow_module('zope.component')
    allow_module('zope.event')
    allow_module("pdb")    
    
    import easyshop.carts.content
    import easyshop.catalog.content
    import easyshop.criteria.content
    import easyshop.customers.content
    import easyshop.discounts.content
    import easyshop.groups.content
    import easyshop.information.content
    import easyshop.payment.content
    import easyshop.order.content
    import easyshop.shipping.content
    import easyshop.shop.content
    import easyshop.stocks.content
    import easyshop.taxes.content
        
    import catalog

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

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])