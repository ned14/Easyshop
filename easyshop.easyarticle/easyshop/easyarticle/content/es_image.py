# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.image import ATImage

# ATContentTypes imports
from Products.ATContentTypes.configuration import zconf

# ATReferenceBrowserWidget imports
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# SmartColorWidget imports
from Products.SmartColorWidget.Widget import SmartColorWidget

# easyarticle imports
from easyshop.easyarticle.config import *
from easyshop.easyarticle.interfaces import IESImage

# easyshop imports
from easyshop.core.interfaces import IShopManagement

schema = Schema((
    StringField(
        "backgroundColor",
        default="#FFFFFF",
        searchable=False,
        widget=SmartColorWidget(
            label="Background Color",
            label_msgid = "schema_background_color_label",		       
            description = "Choose a color for the background.",
            description_msgid = "schema_background_color_description",
            i18n_domain = "EasyArticle")),

    TextField(
        "text",
        searchable=False,
        storage = AnnotationStorage(migrate=True),
        validators = ("isTidyHtmlWithCleanup",),
        default_content_type = zconf.ATDocument.default_content_type,
        default_output_type = "text/x-html-safe",
        allowable_content_types = zconf.ATDocument.allowed_content_types,
        widget = RichWidget(
            label = "Image Text",
            label_msgid = "schema_image_text_label",
            description = "",
            description_msgid = "schema_image_text_description",
            rows = 25,
            i18n_domain = "EasyArticle",
            allow_file_upload = zconf.ATDocument.allow_document_upload)),

    ReferenceField( 
        name='relatedObject',
        multiValued=False,
        relationship='image_object',
        widget=ReferenceBrowserWidget(
            label="Related Object",
            label_msgid="schema_related_object_label",
            description='Please select an object to which the details link will be referring.',
            description_msgid="schema_related_object_description",
            i18n_domain='EasyArticle',            
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            startup_directory="getStartupDirectory",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),        
            
),
)

schema = ATImage.schema.copy() + schema
schema["image"].required = False

class ESImage(ATImage):
    """
    """
    implements(IESImage)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = schema

    def getStartupDirectory(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath())
        
registerType(ESImage, PROJECTNAME)