# zope imports
from zope.interface import Interface

class IInformationContainer(Interface):
    """Marker interface to mark information containers.
    """
    
class IInformationPage(Interface):
    """Marker interface to mark terms and conditions.
    """