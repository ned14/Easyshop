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

# EasyShop imports
from Products.EasyShop.interfaces import ITaxes
from Products.EasyShop.interfaces import IProductManagement
from Products.EasyShop.interfaces import IOrderItemContent
from Products.EasyShop.config import *

schema = Schema((

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

    ReferenceField(
        name='easyshopproducts',
        widget=ReferenceWidget(
            label='Products',
            label_msgid='schema_easyshop_products_label',
            i18n_domain='EasyShop',
        ),
        allowed_types=('Product',),
        multiValued=0,
        relationship='easyshoporderitem_easyshopproduct'
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
     
),
)

class EasyShopOrderItem(BaseContent):
    """An order item holds price, tax and products informations from the moment
    the customer has buyed aka checked out its cart. 
    
    This means it doesn't need any calculations any more.
    """
    implements(IOrderItemContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    security.declarePublic('getProduct')
    def getProduct(self):
        """Returns the product of the item
        """
        try:
            return self.getRefs('easyshoporderitem_easyshopproduct')[0]
        except IndexError:
            return None

    security.declarePublic('setProduct')
    def setProduct(self,product):
        """Sets the product of the item.
        """
        self.addReference(product, "easyshoporderitem_easyshopproduct")

registerType(EasyShopOrderItem, PROJECTNAME)