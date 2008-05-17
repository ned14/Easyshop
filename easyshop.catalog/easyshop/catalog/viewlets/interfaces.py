from zope.viewlet.interfaces import IViewletManager

class IProductsViewletManager(IViewletManager):
    """Viewlet manager for category selector view.
    """

class ICategoriesViewletManager(IViewletManager):
    """Viewlet manager for categories view.
    """

class IProductViewletManager(IViewletManager):
    """Viewlet manager for product view.
    """

class IProductSelectorViewletManager(IViewletManager):
    """Viewlet manager for product selector view.
    """    