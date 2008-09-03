# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# ReferenceBrowserWidget imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IProductSelector
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    BooleanField(
        name = "showTitle",
        languageIndependent=True,
        widget = BooleanWidget(
            label="ShowTitle",
            label_msgid="schema_showtitle_label",
            description = "Select to show title",            
            description_msgid="schema_showtitle_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    ReferenceField(
        name='products', 
        multiValued=1,
        relationship='selectors_products',
        allowed_types=("Product",),
        widget=ReferenceBrowserWidget(
            label="Products",
            label_msgid="schema_products_label",
            description='Please select all products, which should be displayed for this category.',
            description_msgid="schema_products_description",        
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

ProductSelector_schema = BaseSchema.copy() + schema.copy()

class ProductSelector(BaseContent):
    """To select one or more products of a category and its subcategories.
    
    Used to select products which should be displayed on several views, e.g. 
    category view"""
    
    implements(IProductSelector)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ProductSelector_schema

    def getStartupDirectoryForProducts(self):
        """
        """
        shop = IShopManagement(self).getShop()
        shop_path = "/".join(shop.getPhysicalPath())
        
        catalog = getToolByName(self, "portal_catalog")
        brains = catalog.searchResults(
            path = shop_path,
            object_provides = "easyshop.core.interfaces.catalog.IProductsContainer"
        )
        
        if len(brains) > 0:
            products_folder = brains[0]
            return products_folder.getPath()
        else:
            return shop_path
            
registerType(ProductSelector, PROJECTNAME)