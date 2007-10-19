# zope imports
from zope.interface import Interface

class ICartsFolderContent(Interface):
    """A marker interface for carts folder content objects.
    """

class ICategoriesContainer(Interface):
    """A marker interface for categories containers.
    """
    
class ICustomersContainer(Interface):
    """A marker interface for customer folder content objects.
    """

class IGroupsContainer(Interface):
    """Marker interface for group folder content objects.
    """

class IPaymentMethodsContainer(Interface):
    """A marker interface for payment method folder content objects.
    """

class IPaymentPricesContainer(Interface):
    """A marker interface for payment price folder objects.
    """

class IProductsContainer(Interface):
    """Marker interface for product folder content objects.
    """    
    
class IOrdersContainer(Interface):
    """A marker interface for order folder content objects.
    """
        
class IShippingPricesContainer(Interface):
    """A marker interface for shipping prices folder content objects.
    """

class IShippingMethodsContainer(Interface):
    """Marker interface to mark shipping method folder content objects.
    """
    
class ITaxesContainer(Interface):
    """A marker interface for taxes folder.
    """
