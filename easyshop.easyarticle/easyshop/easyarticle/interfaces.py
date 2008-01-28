# zope imports
from zope.interface import Interface

# EasyArticle imports
from Products.EasyArticle.interfaces import IEAReferenceContent

class IESReference(IEAReferenceContent):
    """A marker interface for EasyShop/EasyArticle reference objects.
    """
    
class IESImage(Interface):
    """Marker interface for EasyShop/EasyArticle images.
    """