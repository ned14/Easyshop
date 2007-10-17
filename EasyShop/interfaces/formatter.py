from zope.interface import Interface
    
class IFormatterContent(Interface):
    """Marker interface to mark category content objects.
    
    A formatter provides informations of how products of a shop/category/selector
    are displayed. The first formatter which is found is taken. Is no formatter
    is found default values are taken.
    """

class IFormatterInfos(Interface):
    """Provides methods to get an formater resp. formatter infos.
    """
    
    def getFormatter():
        """Returns the first formatter found in the path. If no one found
        returns None.
        """

    def getFormatInfosAsDict():
        """Returns the infos of the found formatter as dict.
        """

    def getProductHeight():
        """Returns product height of the found formatter.
        """
        
    def getLinesPerPage():
        """Returns lines per page of the found formatter.
        """

    def getProductsPerLine():
        """Returns products per line of the found formatter.
        """

    def getText():
        """Returns the id of the description, which is to be displayed.
        """
        
    def getImageSize():
        """Returns image size of the found formatter.
        """
        
    def hasFormatter():
        """Returns True if the context has a *direct* formater content object.
        """