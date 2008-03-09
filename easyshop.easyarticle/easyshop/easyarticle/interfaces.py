# zope imports
from zope.interface import Interface

class IESReference(Interface):
    """A marker interface for easyshop/easyarticle reference objects.
    """
    
class IESImage(Interface):
    """Marker interface for easyshop/easyarticle images.
    """