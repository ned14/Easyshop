# zope imports
from zope.component import adapts
from zope.interface import implements

# EasyArticle imports
from Products.EasyArticle.interfaces import IData

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.easyarticle.interfaces import IESReference

class ESReferenceData:
    """
    """
    implements(IData)
    adapts(IESReference)

    def __init__(self, context):
        """        
        """
        self.context = context
        
    def getDict(self):
        """
        """
        object = self.context.getObjectReference()
                
        data = {}

        if len(self.context.getText()) != 0:
            text = self.context.getText()
        else:
            text = object.getText()

        if len(self.context.getImage()) != 0:
            image = self.context
        else:
            image = IPhotoManagement(object).getMainPhoto()
        
        if image is not None:
            image_url = image.absolute_url()
                 
        data.update({
            "portal_type" : object.getPortalTypeName(),
            "url"         : object.absolute_url(),
            "title"       : object.Title(),
            "description" : object.Description(),
            "text"        : text,
            "image_url"   : image_url,
            "price"       : "0.0",
        })
                        
        return data