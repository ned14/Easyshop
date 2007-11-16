# zope imports
from zope.interface import Interface

class ICheckoutManagement(Interface):
    """Provides several converter methods for numbers.
    """
    def getNextURL(id):
        """Returns the url of the next step within the checkout process.
        """

    def redirectToNextURL(id):
        """Redirects to the next step within the checkout process.
        """