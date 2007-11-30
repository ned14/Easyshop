# zope imports
from zope.component.exceptions import ComponentLookupError

# iqpp.rating imports
from easyshop.core.interfaces import ICategory

# CMFPlone imports
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

def total_amount_of_products(object, portal, **kwargs):
    try:
        # This has to be done without the help of the catalog. Otherwise it
        # counts before all to counted objects are in the catalog. That is at
        # least the case for Advanced/Update Catalog.
        counter = 0
        # It has to be catalog independent
        if ICategory.providedBy(object):
            counter += len(object.getProducts())
            counter = countCategories(object, counter)
                
        return counter
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('total_amount_of_products',
                            total_amount_of_products)

def amount_of_categories(object, portal, **kwargs):
    try:
        # This has to be done without the help of the catalog. Otherwise it
        # counts before all to counted objects are in the catalog. That is at
        # least the case for Advanced/Update Catalog.
        
        # If we have no categories a non-int will be returned. This helps in the
        # categories portlet to decide whether there are sub categories or not.
        counter = 0
        if ICategory.providedBy(object):
            counter = len(object.objectValues("Category"))

        return counter
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('amount_of_categories',
                            amount_of_categories)
                            
def countCategories(category, counter):
    """
    """
    for category in category.objectValues("Category"):
        counter += len(category.getProducts())
        counter = countCategories(category, counter)
    return counter
    