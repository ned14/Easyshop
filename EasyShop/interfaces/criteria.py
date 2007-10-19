from zope.interface import Interface

class ICriteriaContent(Interface):
    """Marker interface to mark criteria content objects.
    """

class ICategoryCriteria(ICriteriaContent):
    """Marker interface to mark category criteria content objects.
    """
    
class ICountryCriteria(ICriteriaContent):
    """Marker interface to mark country criteria content objects.
    """
            
class ICustomerCriteria(ICriteriaContent):
    """Marker interface to mark customer criteria content objects.
    """

class IDateCriteria(ICriteriaContent):
    """Marker interface to mark date criteria content objects.
    """
    
class IGroupCriteria(ICriteriaContent):
    """Marker interface to mark group criteria content objects.
    """

class IPaymentMethodCriteria(ICriteriaContent):
    """Marker interface to mark payment criteria content objects.
    """
    
class IProductCriteria(ICriteriaContent):
    """Marker interface to mark product criteria content objects.
    """
    
class IPriceCriteria(ICriteriaContent):
    """Marker interface to mark price criteria content objects.
    """

class IShippingMethodCriteria(ICriteriaContent):
    """Marker interface to mark shipping method criteria content objects.
    """
    
class IWeightCriteria(ICriteriaContent):
    """Marker interface to mark weight criteria content objects.
    """
