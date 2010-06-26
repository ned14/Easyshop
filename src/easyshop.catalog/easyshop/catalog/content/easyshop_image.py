# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.image import ATImage

# easyshop imports
from easyshop.core.interfaces import IEasyShopImage
from easyshop.core.interfaces import IImageConversion
from easyshop.core.config import *

schema = Schema((

    StringField(
        name='subtitle',
        widget=StringWidget(
            label='Subtitle',
            label_msgid='schema_subtitle_label',
            description="A subtitle for the image",
            description_msgid="schema_subtitle_description",            
            i18n_domain='EasyShop',
        )
    ),
),
)

class EasyShopImage(ATImage):
    """An extended image for EasyShop.
    """
    implements(IEasyShopImage)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATImage.schema.copy() + schema

    def manage_afterPUT(self, data, marshall_data, file, context, mimetype,
                        filename, REQUEST, RESPONSE):
        """Overwritten to set image.
        """
        file.seek(0)
        self.setImage(file)
        
    def setImage(self, data, **kwargs):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        super(EasyShopImage, self).setImage(data)

registerType(EasyShopImage, PROJECTNAME)