# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# EasyShop imports
from Products.EasyShop.interfaces import IGroupContent
from Products.EasyShop.config import *

schema = Schema((
    TextField(
        name='description',
        widget=TextAreaWidget(
            label='Description',
            label_msgid='schema_help_description',
            description="A short summary of the content",
            description_msgid="schema_help_description",            
            i18n_domain='plone',
        )
    ),
    
    ReferenceField( 
        name='easyshopproducts', 
        multiValued=1,
        relationship='easyshopgroup_easyshopproduct',
        allowed_types=("Product",),
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

class ProductGroup(BaseFolder):
    """Arrange products to a group, which can be associated with taxes, 
    discounts, etc. A group is invisible for customers.
    """
    implements(IGroupContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getStartupDirectoryForProducts(self):
        """
        """
        shop = self.getShop()
        return "/".join(shop.getPhysicalPath()) + "/products"

registerType(ProductGroup, PROJECTNAME)