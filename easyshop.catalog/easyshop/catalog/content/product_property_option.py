# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IPropertyOption

schema = Schema((
    ImageField(
        name='image',
        sizes= {'listing' :  (16, 16)},
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),
    
    FloatField(
        name='price',
        default=0.0,
        widget=DecimalWidget(
            size="10",
            label='Price',
            label_msgid='schema_price_label',
            i18n_domain='EasyShop',
        )
    ),
    
))

class ProductPropertyOption(BaseContent):
    """
    """
    implements(IPropertyOption)
    schema = BaseContent.schema.copy() + schema
        
registerType(ProductPropertyOption, PROJECTNAME)