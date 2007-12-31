# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# DataGridField imports
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

# easyshop imports
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IOrderItem
from easyshop.core.config import *

schema = Schema((

    ReferenceField(
        name='product',
        allowed_types=('Product',),
        multiValued=0,
        relationship='orderitem_product',
        widget=ReferenceWidget(
            label='Product',
            label_msgid='schema_easyshop_products_label',
            i18n_domain='EasyShop',
        ),        
    ),

    # The product name. Will be used if the product has been deleted in the
    # meanwhile.
    StringField(
        name="productTitle",
        widget=StringWidget(
            label="Product Title",
            label_msgid="schema_product_title_label",
            i18n_domain="EasyShop",
        ),
    ),

    # The internal article id. will be used if the product has been deleted in
    # the meanwhile.
    StringField(
        name="articleId",
        widget=StringWidget(
            label="Article ID",
            label_msgid="schema_product_id_label",
            i18n_domain="EasyShop",
        ),
    ),
    
    FloatField(
        name='productQuantity',
        widget=DecimalWidget(
            label='Product Quantity',
            label_msgid='schema_product_quantity_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='productPriceGross',
        widget=DecimalWidget(
            label='Product Price Gross',
            label_msgid='schema_product_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='productPriceNet',
        widget=DecimalWidget(
            label='Product Price Net',
            label_msgid='schema_product_price_net_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='productTax',
        widget=DecimalWidget(
            label='Product Tax',
            label_msgid='schema_product_tax_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='priceGross',
        widget=DecimalWidget(
            label='Price Gross',
            label_msgid='schema_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='priceNet',
        widget=DecimalWidget(
            label='Price Net',
            label_msgid='schema_price_net_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='taxRate',
        widget=DecimalWidget(
            label='Tax Rate',
            label_msgid='schema_tax_rate_label',
            i18n_domain='EasyShop',
        )
    ),

    FloatField(
        name='tax',
        widget=DecimalWidget(
            label='Tax',
            label_msgid='schema_tax_label',
            i18n_domain='EasyShop',
        )
    ),

    DataGridField('properties',
            searchable = True,
            columns=("title", "selected_option", "price"),
            widget = DataGridWidget(
                columns={
                    'title'           : Column("Title"),
                    'selected_option' : Column("Selected Option"),
                    'price'           : Column("Price"),                    
                },
             ),
     ),

    StringField(
        name="discountDescription",
        widget=StringWidget(
            label="Discount Description",
            label_msgid="schema_discount_description_label",
            i18n_domain="EasyShop",
        ),
    ),

    FloatField(
        name='discountNet',
        default=0.0,
        widget=DecimalWidget(
            label="Discount Net",
            label_msgid="schema_discount_net_label",
            i18n_domain="schema",
        ),
    ),

    FloatField(
        name='discountGross',
        default=0.0,
        widget=DecimalWidget(
            label="Discount Gross",
            label_msgid="schema_discount_gross_label",
            i18n_domain="schema",
        ),
    ),
         
),
)

class OrderItem(BaseContent):
    """An order item holds price, tax and products informations from the moment
    the customer has buyed aka checked out its cart. This means it doesn't need
    any calculations any more.
    """
    implements(IOrderItem)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    security.declarePublic('getProduct')
    def getProduct(self):
        """Returns the product of the item
        """
        try:
            return self.getRefs('orderitem_product')[0]
        except IndexError:
            return None

    security.declarePublic('setProduct')
    def setProduct(self,product):
        """Sets the product of the item.
        """
        self.addReference(product, "orderitem_product")

registerType(OrderItem, PROJECTNAME)