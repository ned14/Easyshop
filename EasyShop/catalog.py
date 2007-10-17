# zope imports
from zope.component.exceptions import ComponentLookupError

# iqpp.rating imports
from Products.EasyShop.interfaces import ICategoryContent

# CMFPlone imports
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

def total_amount_of_products(object, portal, **kwargs):
    try:
        # This has to be done without the help of the catalog. Otherwise it
        # counts before all to counted objects are in the catalog. That is at
        # least the case for Advanced/Update Catalog.
        counter = 0
        # It has to be catalog independent
        if ICategoryContent.providedBy(object):
            counter += len(object.getEasyshopproducts())
            counter = countCategories(object, counter)
                
        return counter
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('total_amount_of_products',
                            total_amount_of_products)
                            
def countCategories(category, counter):
    """
    """
    for category in category.objectValues("EasyShopCategory"):
        counter += len(category.getEasyshopproducts())
        counter = countCategories(category, counter)
    return counter
    