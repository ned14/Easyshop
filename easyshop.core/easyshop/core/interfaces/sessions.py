# zope imports
from zope.interface import Interface

class ISessionManagement(Interface):
    """
    """
    def getSID(request):
        """Returns the current session id.
        """