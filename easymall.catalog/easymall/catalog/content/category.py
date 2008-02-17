# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# easyshop imports
from easyshop.catalog.content.category import Category as ShopCategory
from easyshop.core.config import *
from easyshop.core.interfaces import IImageConversion

# easyshop imports
from easymall.mall.config import *
from easymall.mall.interfaces import IMallCategory
from easymall.mall.interfaces import IMallManagement

schema = Schema((
    ReferenceField( 
        name='products', 
        multiValued=1,
        relationship='mall_categories_products',
        allowed_types=("MallProduct",),
        widget=ReferenceBrowserWidget(        
            label='Products',
            label_msgid='schema_products_label',
            description='Please select all products, which should associated with this category.',
            description_msgid="schema_products_description",
            i18n_domain='EasyShop',                    
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForProducts",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),    
    
),
)

schema = ShopCategory.schema.copy() + schema

class MallCategory(ShopCategory):
    """A mall category is category which is provided by the mall. 
    
    Please note: 
       - A mall category exists additionally to default shop categories.
       - A mall product is a replacement for the default shop product.
    """
    implements(IMallCategory)
    schema = schema

    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)        

    def getStartupDirectoryForProducts(self):
        """
        """
        mall = IMallManagement(self).getMall()
        return "/".join(mall.getPhysicalPath())

registerType(MallCategory, PROJECTNAME)