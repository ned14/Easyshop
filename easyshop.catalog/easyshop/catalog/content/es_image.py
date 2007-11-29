# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.image import ATImage

# ReferenceBrowserWidget imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IESImage
from easyshop.core.interfaces import IImageConversion
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    ReferenceField(
        name='content', 
        multiValued=0,
        relationship='image_content',
        widget=ReferenceBrowserWidget(
            label="Link To Content",
            label_msgid="schema_products_label",
            description='Please select a content object to which you want to link to.',
            description_msgid="schema_content_description",        
            show_path=1,
            allow_search=1, 
            allow_browse=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForContent",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),
    
),
)

class ESImage(ATImage):
    """A extended image for EasyShop.
    """
    implements(IESImage)
    schema = ATImage.schema.copy() + schema.copy()

    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        
        super(ESImage, self).setImage(data)

    def getStartupDirectoryForContent(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath())
        
registerType(ESImage, PROJECTNAME)