# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# DataGridField imports
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IPropertyContent

schema = Schema((
       DataGridField('Options',
                searchable = True,
                columns=("name", "price"),
                widget = DataGridWidget(
                    columns={
                        'name'  : Column("Name"),
                        'price' : Column("Price"),
                    },
                 ),
         ),
),
)

class ProductProperty(BaseContent):
    """
    """
    implements(IPropertyContent)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

registerType(ProductProperty, PROJECTNAME)