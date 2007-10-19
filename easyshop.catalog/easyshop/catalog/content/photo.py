# Python imports
from StringIO import StringIO

# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.image import ATImage

# EasyShop imports
from Products.EasyShop.content.shop import EasyShopBase
from Products.EasyShop.interfaces import IProductPhotoContent
from Products.EasyShop.interfaces import IImageConversion
from Products.EasyShop.config import *

schema = Schema((

    ImageField(
        name='image',
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

    BooleanField(
        name = "cutImage",
        widget = BooleanWidget(
            label="Cut Image",
            label_msgid="schema_cut_image_label",
            description = "Select, to cut the image.",  
            description_msgid="schema_cut_image_label_description",
            i18n_domain="EasyShop",
        ),
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

class Photo(BaseContent, EasyShopBase):
    """A photo for a product.
    """
    implements(IProductPhotoContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def manage_afterPUT(self, data, marshall_data, file, context, mimetype,
                        filename, REQUEST, RESPONSE):
        """Overwritten to set image.
        """
        file.seek(0)
        self.setImage(file)
        
    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)

registerType(Photo, PROJECTNAME)