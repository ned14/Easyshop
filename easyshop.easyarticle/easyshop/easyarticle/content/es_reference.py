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
            i18n_domain='EasyShop',
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectory",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"})),
    TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
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
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),
),
)

schema = BaseSchema.copy() + schema.copy()
schema["title"].required = False

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

registerType(ESReference, PROJECTNAME)