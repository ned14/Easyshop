from zope.viewlet.interfaces import IViewletManager

class ICategoryViewletManager(IViewletManager):
    """Viewlet manager for category selector view.
    """

class IProductViewletManager(IViewletManager):
    """Viewlet manager for product view.
    """
    
class IProductSelectorViewletManager(IViewletManager):
    """Viewlet manager for product selector view.
    """    