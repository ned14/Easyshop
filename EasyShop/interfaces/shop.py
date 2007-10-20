from zope.interface import Interface

class IShopContent(Interface):
    """Marker interface to mark shop content objects.
    """
    
class IShopInformation(Interface):
    """Methods which provide information of an shop.
    """
    def getTermsAndConditions():
        """Returns terms and conditions as file and text.
        """