# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATFolder

# ATBackRef imports
from Products.ATBackRef.BackReferenceField import *

# ATReferenceBrowserWidget imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# easyshop imports
from easymall.mall.config import *
from easyshop.catalog.content.product import Product as ShopProduct

# easymall imports
from easymall.mall.interfaces import IMallManagement
from easymall.mall.interfaces import IMallProduct

schema = Schema((

    BackReferenceField(
        name='mallCategories',
        multiValued=1,
        relationship='mall_categories_products',
        allowed_types=("Category",),
        widget=BackReferenceBrowserWidget(
            label="Mall Categories",
            label_msgid="schema_mall_categories_label",
            description='Please select all catgories, which should be associated with this product.',
            description_msgid="schema_mall_categories_description",        
            i18n_domain='EasyShop',            
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,             
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForMallCategories",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),        
    
),
)

schema = ShopProduct.schema.copy() + schema

class MallProduct(ShopProduct):
    """A Mall Product has additional mall categories.
    """
    implements(IMallProduct)
    schema = schema

    def getStartupDirectoryForMallCategories(self):
        """
        """
        mall = IMallManagement(self).getMall()
        return "/".join(mall.getPhysicalPath()) + "/categories"

registerType(MallProduct, PROJECTNAME)