# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.base import ATCTMixin

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IGenericPaymentMethod

schema = Schema((
    TextField(
        name = "note",
        widget=TextAreaWidget(
            label = "Note",
            description = "This text will be displayed on the invoice",
            label_msgid = "schema_note_label",
            description_msgid = "schema_note_description",
            i18n_domain = "EasyShop"),
    ),
    
    BooleanField(
        name = "payed",
        languageIndependent=True,
        widget = BooleanWidget(
            label="Payed",
            label_msgid="schema_payment_state_label",
            description = "If checked, the order state will set to payed.",
            description_msgid="schema_payment_state_description",
            i18n_domain="EasyShop",
        ),
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
),
)

schema = ATCTMixin.schema.copy() + schema.copy()
schema["title"].required = False

class GenericPaymentMethod(OrderedBaseFolder):
    """A generic payment method.
    """
    implements(IGenericPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = schema

registerType(GenericPaymentMethod, PROJECTNAME)