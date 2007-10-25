# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATBackRef imports
from Products.ATBackRef.BackReferenceField import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShopManagement
from easyshop.catalog.content.product import Product
from easyshop.product_reference.interfaces import IProductReference


schema = Schema((
    ReferenceField( 
        name='objectReference', 
        required=True,
        multiValued=0,
        relationship='easyarticle_object',
        widget=ReferenceBrowserWidget(
            label='Object',
            label_msgid='schema_object_reference_label',
            description='',
            description_msgid="schema_object_reference_description",
            i18n_domain='EasyShop',                    
            show_path=1,
            allow_search=1, 
            allow_browse=1,
            startup_directory="getStartupDirectoryForObject",
            available_indexes={'SearchableText':'Free text search'},
            ),    
    ),    
))

schema = schema.copy() + Product.schema.copy()
schema["title"].required = False
schema["title"].widget.visible = {'view':'invisible', 'edit':'invisible'}
schema["description"].widget.visible = {'view':'invisible', 'edit':'invisible'}
schema["text"].widget.visible = {'view':'invisible', 'edit':'invisible'}

class ProductReference(Product):
    """A ProductReference makes arbitrary objects buyable.
    """
    implements(IProductReference)
    schema = schema
    
    def Title(self):
        """
        """
        try:
            return self.getObjectReference().Title()
        except AttributeError:
            return ""

    def Description(self):
        """
        """
        try:
            return self.getObjectReference().Description()
        except AttributeError:
            return ""

    def getText(self):
        """
        """
        try:
            return self.getObjectReference().getText()
        except AttributeError:
            return ""
                        
    def getStartupDirectoryForObject(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath())

registerType(ProductReference, PROJECTNAME)