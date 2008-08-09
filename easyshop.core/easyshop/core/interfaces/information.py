# zope imports
from zope.interface import Interface
from zope import schema

# Message factory
from easyshop.core.config import _

class IInformationContainer(Interface):
    """A container to hold information like terms and conditions.
    """
    
class IInformationPage(Interface):
    """A page to hold the information as HTML and downloadable file.
    """
    text = schema.Text(
        title=_(u'Text'),
        description=_(u"The information as HTML"),
        default=u'',
        required=False,
    )

    text = schema.Bytes(
        title=_(u'File'),
        description=_(u"The information as downloadable file."),
        required=False,
    )
    
    
class IInformationManagement(Interface):
    """Provides methods to manage information pages.
    """
    def getInformationPage(id):
        """Returns information page by given id
        """
        
    def getInformationPages():
        """Returns all information pages.
        """
        
    def getInformationPagesFor(product):
        """Returns valid information pages for given product.
        """