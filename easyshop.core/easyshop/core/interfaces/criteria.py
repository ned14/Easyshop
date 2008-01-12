# zope imports
from zope.interface import Interface

class ICriteria(Interface):
    """Base interface for criteria.
    """
    def getValue():
        """Returns the entered value for the criterion.
        """
         
class ICategoryCriteria(ICriteria):
    """Marker interface to mark category criteria content objects.
    """
    
class ICountryCriteria(ICriteria):
    """Marker interface to mark country criteria content objects.
    """
            
class ICustomerCriteria(ICriteria):
    """Marker interface to mark customer criteria content objects.
    """

class IDateCriteria(ICriteria):
    """Marker interface to mark date criteria content objects.
    """
    
class IGroupCriteria(ICriteria):
    """Marker interface to mark group criteria content objects.
    """

class IPaymentMethodCriteria(ICriteria):
    """Marker interface to mark payment criteria content objects.
    """

class IProductAmountCriteria(ICriteria):
    """Marker interface to mark product amount criteria content objects.
    """

class IProductCriteria(ICriteria):
    """Marker interface to mark product criteria content objects.
    """
    
class IPriceCriteria(ICriteria):
    """Marker interface to mark price criteria content objects.
    """

class IShippingMethodCriteria(ICriteria):
    """Marker interface to mark shipping method criteria content objects.
    """

class IStockAmountCriteria(ICriteria):
    """Marker interface to mark stock criteria content objects.
    """
    
class IWeightCriteria(ICriteria):
    """Marker interface to mark weight criteria content objects.
    """
