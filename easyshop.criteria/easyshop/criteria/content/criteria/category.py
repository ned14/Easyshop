# zope imports
import transaction
from zope.interface import implements

# Zope imports
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import ICategoryCriteriaContent

schema = Schema((

    StringField(
        name='title',
        widget=StringWidget(
            visible={'edit':'invisible', 'view':'invisible'},
            label='Title',
            label_msgid='schema_title_label',
            i18n_domain='EasyShop',
        ),
        required=0
    ),

    LinesField(
        name='categories',
        widget=MultiSelectionWidget(
            label='Categories',
            label_msgid='schema_categories_label',
            i18n_domain='EasyShop',
        ),
        multiValued=1,
        vocabulary="getCategoriesAsDL"
    ),

),
)

class EasyShopCategoryCriteria(BaseContent):
    """
    """
    implements(ICategoryCriteriaContent)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def getCategoriesAsDL(self):
        """Returns all Categories as DisplayList
        """
        dl = DisplayList()
        catalog = getToolByName(self, "portal_catalog")

        for category in catalog.searchResults(
            portal_type="EasyShopCategory",
            sort_on = "getObjPositionInParent"):
            dl.add(category.id, category.Title)
        return dl

    def Title(self):
        """
        """
        return "Category"

    def getValue(self):
        """
        """
        return ", ".join(self.getCategories())

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = "CategoryCriteria"
        self.setId(new_id)
        
registerType(EasyShopCategoryCriteria, PROJECTNAME)