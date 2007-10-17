from zope.interface import Interface

class ICriteriaContent(Interface):
    """Marker interface to mark criteria content objects.
    """

class ICategoryCriteriaContent(ICriteriaContent):
    """Marker interface to mark category criteria content objects.
    """
    
class ICountryCriteriaContent(ICriteriaContent):
    """Marker interface to mark country criteria content objects.
    """
            
class ICustomerCriteriaContent(ICriteriaContent):
    """Marker interface to mark customer criteria content objects.
    """

class IDateCriteriaContent(ICriteriaContent):
    """Marker interface to mark date criteria content objects.
    """
    
class IGroupCriteriaContent(ICriteriaContent):
    """Marker interface to mark group criteria content objects.
    """

class IPaymentMethodCriteriaContent(ICriteriaContent):
    """Marker interface to mark payment criteria content objects.
    """
    
class IProductCriteriaContent(ICriteriaContent):
    """Marker interface to mark product criteria content objects.
    """
    
class IPriceCriteriaContent(ICriteriaContent):
    """Marker interface to mark price criteria content objects.
    """

class IShippingMethodCriteriaContent(ICriteriaContent):
    """Marker interface to mark shipping method criteria content objects.
    """
    
class IWeightCriteriaContent(ICriteriaContent):
    """Marker interface to mark weight criteria content objects.
    """
