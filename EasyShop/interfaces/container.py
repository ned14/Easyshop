# zope imports
from zope.interface import Interface

class ICartsFolderContent(Interface):
    """A marker interface for carts folder content objects.
    """

class ICategoryFolderContent(Interface):
    """A marker interface for categories containers.
    """
    
class ICustomerFolderContent(Interface):
    """A marker interface for customer folder content objects.
    """

class IGroupFolderContent(Interface):
    """Marker interface for group folder content objects.
    """

class IPaymentMethodsFolderContent(Interface):
    """A marker interface for payment method folder content objects.
    """

class IPaymentPricesFolderContent(Interface):
    """A marker interface for payment price folder objects.
    """

class IProductFolderContent(Interface):
    """Marker interface for product folder content objects.
    """    
    
class IOrderFolderContent(Interface):
    """A marker interface for order folder content objects.
    """
        
class IShippingPricesFolderContent(Interface):
    """A marker interface for shipping prices folder content objects.
    """

class IShippingMethodsFolderContent(Interface):
    """Marker interface to mark shipping method folder content objects.
    """
    
class ITaxFolderContent(Interface):
    """A marker interface for taxes folder content objects.
    """
