# Python imports
from StringIO import StringIO

# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.ATContentTypes.content.image import ATImage
try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.interfaces import IProductPhoto
from easyshop.core.interfaces import IImageConversion
from easyshop.core.config import *

schema = Schema((

    ImageField(
        name='image',
        languageIndependent=True,
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),

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

class Photo(BaseContent):
    """A photo for a product.
    """
    implements(IProductPhoto)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

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
        self.getField("image").set(self, data)

registerType(Photo, PROJECTNAME)