# zope imports
from zope.component.exceptions import ComponentLookupError

# iqpp.rating imports
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct

# CMFPlone imports
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

def total_amount_of_products(object, portal, **kwargs):
    try:
        # This has to be done without the help of the catalog. Otherwise it
        # counts before all to counted objects are in the catalog. That is at
        # least the case for Advanced/Update Catalog.

        counter = 0
        if ICategory.providedBy(object):
            counter += len(object.getProducts())
            counter = countCategories(object, counter)
                
        return counter
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('total_amount_of_products', total_amount_of_products)

def amount_of_categories(object, portal, **kwargs):
    try:
        # This has to be done without the help of the catalog. Otherwise it
        # counts before all to counted objects are in the catalog. That is at
        # least the case for Advanced/Update Catalog.
        
        counter = 0
        if ICategory.providedBy(object):
            counter = len(object.objectValues("Category"))

        return counter
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('amount_of_categories', amount_of_categories)

def categories(object, portal, **kwargs):
    """Indexes all categories and parent categories of a product.
    """
    try:
        result = {}
        if IProduct.providedBy(object):
            for category in ICategoryManagement(object).getTopLevelCategories():
                result[category.UID()] = 1
                
                # Collect parent categories
                object = category
                while object is not None:
                    result[object.UID()] = 1
                    object = object.getParentCategory()
            
        return result.keys()
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('categories', categories)

def countCategories(category, counter):
    """
    """
    for category in category.objectValues("Category"):
        counter += len(category.getProducts())
        counter = countCategories(category, counter)
    return counter
    
def getParentCategory(object, portal, **kwargs):
    try:
        if ICategory.providedBy(object):
            parent_category = object.getParentCategory()
            if parent_category is not None:
                return parent_category.UID()
            else: 
                return None
        
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

registerIndexableAttribute('getParentCategory', getParentCategory)
    