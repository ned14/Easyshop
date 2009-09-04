from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTMixin
from easyshop.core.config import PROJECTNAME
from easyshop.mpay24.interfaces import ImPAY24PaymentMethod
from easyshop.mpay24 import EasyShopMPAY24MessageFactory as _

schema = Schema((
    
    StringField(
        name="url",
        validators=('isURL',),
        required=True,
    ),
    
    IntegerField(
        name="merchant_id",
        required=True,
        size="7",
    ),
    
    TextField(
        name="mdxi",
        required=True,
        default_output_type='text/xml',
        widget=TextAreaWidget(
            label=_("MDXI"),
            description=_("Merchant Data Exchange Interface (XML Format)\nUse %(tid)s, %(price)s, %(site_url)s to replace cart values")
        ),
    ),
    
    TextField(
        name = "note",
        widget=TextAreaWidget(
            label = "Note",
            description = "This text will be displayed on the invoice",
            label_msgid = "schema_note_label",
            description_msgid = "schema_note_description",
            i18n_domain = "EasyShop"),
    ),

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
    
))

class mPAY24PaymentMethod(OrderedBaseFolder):
    """
    """
    implements(ImPAY24PaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy() + schema


registerType(mPAY24PaymentMethod, PROJECTNAME)