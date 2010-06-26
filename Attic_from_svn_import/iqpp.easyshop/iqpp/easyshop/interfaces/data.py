# zope imports
from zope.interface import Interface

class IData(Interface):
    """Provides methods to return content objects in several formats.
    """
    def asDict():
        """Returns context's attributes as dict.
        """