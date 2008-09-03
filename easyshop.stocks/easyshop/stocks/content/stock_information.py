# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IStockInformation

schema = Schema((

    BooleanField(
        name='available',
        widget=BooleanWidget(
            label='Available',
            label_msgid='schema_available_label',
            description = "Marks the products as available or not available",
            description_msgid = "schema_available_description",
            i18n_domain='EasyShop',
        )
    ),
    
    StringField(
        name="deliveryTimeMin",
        vocabulary=DELIVERY_TIMES_MIN,
        widget=SelectionWidget(
            label="Minimum Delivery Time",
            label_msgid="schema_delivery_time_min_label",
            description = "The minimum time period of shipping.",
            description_msgid = "schema_delivery_time_min_description",            
            i18n_domain="EasyShop",        
        ),
    ),

    StringField(
        name="deliveryTimeMax",
        vocabulary=DELIVERY_TIMES_MAX,
        widget=SelectionWidget(
            label="Maximum Delivery Time",
            label_msgid="schema_delivery_time_max_label",
            description = "The maximum time period of shipping.",
            description_msgid = "schema_delivery_time_max_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name="deliveryTimeUnit",
        vocabulary=DELIVERY_TIMES_UNIT,
        default=u"Days",
        widget=SelectionWidget(
            label="Delivery Time Unit",
            label_msgid="schema_delivery_time_unit_label",
            description = "The unit of the above selected minimum and maximum delivery time.",
            description_msgid = "schema_delivery_time_unit_description",
            i18n_domain="EasyShop",        
        ),
    ),

    ImageField(
        name='image',
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),

),
)

class StockInformation(OrderedBaseFolder):
    """
    """
    implements(IStockInformation)
    schema = OrderedBaseFolderSchema.copy() + schema.copy()
    _at_rename_after_creation = True

registerType(StockInformation, PROJECTNAME)