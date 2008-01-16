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
from easyshop.core.config import *
from easyshop.core.interfaces import IProperty

schema = Schema((
       DataGridField('Options',
                searchable = True,
                columns=("id", "name", "price"),
                widget = DataGridWidget(
                    columns={
                        "id"    : Column("Id"),
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
    implements(IProperty)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

registerType(ProductProperty, PROJECTNAME)