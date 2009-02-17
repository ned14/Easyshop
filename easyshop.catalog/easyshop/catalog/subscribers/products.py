# zope imports
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.component import adapter

# easyshop imports
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant

@adapter(IProduct, IObjectModifiedEvent)
def clearCache(product, event):
    """
    """
    if hasattr(product, "cache"):
        product.cache.clear()
        
    if IProductVariant.providedBy(product):
        product = product.aq_inner.aq_parent
        if hasattr(product, "cache"):
            product.cache.clear()
        