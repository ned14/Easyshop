# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.document import ATDocumentSchema

# drako.knowledgebase imports
from easyshop.core.config import *
from easyshop.core.interfaces import IInformationPage

schema = ATFolderSchema.copy() + ATDocumentSchema.copy() + Schema ((
    FileField(
        name='file',
        widget=FileWidget(
            label="File",
            label_msgid='schema_file_label',
            description = "Upload of the original document.",
            description_msgid = "schema_file_description",            
            i18n_domain="EasyShop",
        ),
    ),            
))

finalizeATCTSchema(schema, moveDiscussion=False)
class InformationPage(ATFolder):
    """
    """
    implements(IInformationPage)
    _at_rename_after_creation = True
    schema = schema

registerType(InformationPage, PROJECTNAME)