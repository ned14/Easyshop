# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IFormatter

schema = Schema((

    StringField(
        name="title",
        accessor="Title",
        required=False,
        widget=StringWidget(
            visible = {'view':'invisible', 'edit':'invisible'},
        ),
    ),
    
    IntegerField(
        name='linesPerPage',
        default=1,
        widget=IntegerWidget(
            label="Lines Per Page",
            label_msgid="schema_lines_per_page_label",
            description = "",
            description_msgid="schema_lines_per_page_description",
            i18n_domain="EasyShop",
        ),
    ),

    IntegerField(
        name='productsPerLine',
        default=2,
        widget=IntegerWidget(
            label="Products Per Line",
            label_msgid="schema_products_per_line_label",
            description = "",
            description_msgid="schema_products_per_line_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name="imageSize",
        vocabulary="_getImagesSizesAsDL",
        default="mini",
        widget=SelectionWidget(
            label="Image Sizes",
            label_msgid="schema_image_sizes_label",
            description = "The sizes of images",
            description_msgid="schema_image_sizes_description",
            i18n_domain="Products",        
        ),
    ),

    IntegerField(
        name='productHeight',
        default=0,
        widget=IntegerWidget(
            label="Product Height",
            label_msgid="schema_product_height",
            description = "",
            description_msgid="schema_product_height_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name="text",
        vocabulary="_getTextAsDL",
        default="short_text",
        widget=SelectionWidget(
            label="Decription",
            label_msgid="schema_text_label",
            description = "Which text is to be displayed.",
            description_msgid="schema_text_description",
            i18n_domain="Products",        
        ),
    ),    
))    

class Formatter(BaseContent):
    """
    """
    implements(IFormatter)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseContent.schema.copy() + schema

    def Title(self):
        """
        """
        return "Formatter"
        
    def _getImagesSizesAsDL(self):
        """Returns the sizes of images.
        """
        sizes = IMAGE_SIZES.keys()
        sizes.sort(lambda a, b: cmp(IMAGE_SIZES[a][0], IMAGE_SIZES[b][0]))
        
        dl = DisplayList()        
        for size in sizes:
            dl.add(size, size)

        return dl

    def _getTextAsDL(self):
        """Returns ids of available descriptions
        """
        dl = DisplayList()
                
        for text in TEXTS:
            dl.add(text[0], text[1])
        
        return dl
        
registerType(Formatter, PROJECTNAME)