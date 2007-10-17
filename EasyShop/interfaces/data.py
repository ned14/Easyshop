# zope imports
from zope.interface import Interface

class IData(Interface):
    """Provides methods to return data in several formats.
    """
    def asDict():
        """Returns context data as dict.
        """
        # Used in serveral Views.