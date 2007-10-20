# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import ATDocumentSchema

# drako.knowledgebase imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IInformationPage

schema = ATDocumentSchema.copy() + Schema ((    
    FileField(
        name='file',
        widget=FileWidget(
            label="Terms and Conditions",
            label_msgid='schema_terms_and_conditions_label',
            description = "Upload of the original document.",
            description_msgid = "schema_terms_and_conditions_description",            
            i18n_domain="EasyShop",
        ),
    ),            
))

finalizeATCTSchema(schema, moveDiscussion=False)
class InformationPage(ATDocument):
    """
    """
    implements(IInformationPage)
    _at_rename_after_creation = True
    schema = schema

registerType(InformationPage, PROJECTNAME)