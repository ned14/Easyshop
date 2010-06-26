# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# ATContentTypes imports
from Products.ATContentTypes.configuration import zconf

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# easyshop imports
from easyshop.core.interfaces import IShopManagement

# easyshop.easyshop imports
from easyshop.easyarticle.config import *
from easyshop.easyarticle.interfaces import IESReference

schema = Schema((
    BooleanField(
        name="overwriteTitle",
        languageIndependent=True,
        widget = BooleanWidget(
            label="Overwrite Title",
            label_msgid="schema_overwrite_title_label",
            description = "If selected the title from this reference is taken. Otherwise the title of the referenced object.",  
            description_msgid="schema_overwrite_text_title",
            i18n_domain="EasyArticle",
        ),
    ),

    ReferenceField(
        name='objectReference',
        multiValued=0,
        relationship='easyarticle_object',
        allowed_types=("Product", "Category"),
        widget=ReferenceBrowserWidget(
            label="Object",
            label_msgid="schema_object_label",
            description="",
            description_msgid="schema_object_description",
            i18n_domain='EasyArticle',
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectory",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"})),
                               
    BooleanField(
        name="overwriteText",
        languageIndependent=True,
        widget = BooleanWidget(
            label="Overwrite Text",
            label_msgid="schema_overwrite_text_label",
            description = "If selected the text from this reference is taken. Otherwise the text of the referenced object.",
            description_msgid="schema_overwrite_text_description",
            i18n_domain="EasyArticle",
        ),
    ),
                               
    TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              default_content_type = zconf.ATDocument.default_content_type,
              default_output_type = 'text/x-html-safe',
              allowable_content_types = zconf.ATDocument.allowed_content_types,
              widget = RichWidget(
                        description = "",
                        description_msgid = "help_body_text",
                        label = "Body Text",
                        label_msgid = "label_body_text",
                        rows = 25,
                        i18n_domain = "EasyArticle",
                        allow_file_upload = zconf.ATDocument.allow_document_upload)),
    ImageField(
        name='image',
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyArticle',
        ),
        storage=AttributeStorage()
    ),

    StringField(
        name="imageSize",
        vocabulary="_getImageSizesAsDL", 
        default="formatter",   
        widget=SelectionWidget(
            label="Image Size",
            label_msgid="schema_image_size_label",
            description = "",
            description_msgid = "schema_image_size_description",
            i18n_domain="EasyArticle",        
        ),
    ),
    
),
)

schema = BaseSchema.copy() + schema.copy()

schema["title"].required = False
schema.moveField('title', after='overwriteTitle')

class ESReference(BaseContent):
    """A reference for EasyShop.
    """
    implements(IESReference)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = schema
    
    def SearchableText(self):
        """
        """
        # Not this object will be unindex by the parent article
        # After the parent article has taken the SearchableText
        try:
            return self.getObjectReference().SearchableText()
        except AttributeError:
            return ""
            
    def reindexObject(self, idxs=[]):
        """
        """
        # Parent articel takes SearchableText and unindex this object
        self.aq_parent.reindexObject(idxs)

    def getStartupDirectory(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath())

    def _getImageSizesAsDL(self):
        """
        """
        dl = DisplayList()
        dl.add("formatter", "Formatter")
        dl.add("preview"  , "Preview")
        dl.add("mini"     , "Mini")
        dl.add("thumb"    , "Thumb")
        dl.add("title"    , "Title")
        dl.add("icon"     , "Icon")
        dl.add("listing"  , "Listing")
        
        return dl

registerType(ESReference, PROJECTNAME)