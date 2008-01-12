# zope imports
from zope.interface import Interface

class ICopyManagement(Interface):
    """Provides copying of shop content.
    """
    def copyTo(target=None, new_id=None):
        """Copys context to target with give new id.
        """

    def moveTo(target=None, new_id=None):
        """Moves context to target with give new id.
        """
