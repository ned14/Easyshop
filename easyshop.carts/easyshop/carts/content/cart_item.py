# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# DataGridField imports
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

# easyshop imports
from easyshop.core.interfaces import ICartItem
from easyshop.carts.config import PROJECTNAME

schema = Schema((

    IntegerField(
        name='amount',
        default="1",
        widget=IntegerWidget(
            label='Amount',
            label_msgid='schema_amount_label',
            i18n_domain='EasyShop',
        )
    ),

    DataGridField('properties',
            searchable = True,
            columns=("id", "selected_option"),
            widget = DataGridWidget(
                columns={
                    'id'              : Column("ID"),
                    'selected_option' : Column("Selected Option"),
                },
             ),
     ),

    ReferenceField(
        name='easyshopproduct',
        widget=ReferenceWidget(
            label='Product',
            label_msgid='schema_easyshop_products_label',
            i18n_domain='EasyShop',
        ),
        allowed_types=('Product',),
        multiValued=0,
        relationship='CartItem_easyshopproduct'
    ),
),
)

class CartItem(BaseContent):
    """A cart item holds a product, the quantity of the product and the 
    choosen properties.
    """
    implements(ICartItem)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getProduct(self):
        """Returns product of the item or None.
        """
        try:
            return self.getRefs('CartItem_easyshopproduct')[0]
        except IndexError:
            return None

    def setProduct(self, product):
        """Sets the product of the cart item.
        """
        self.addReference(product, "CartItem_easyshopproduct")
                
registerType(CartItem, PROJECTNAME)