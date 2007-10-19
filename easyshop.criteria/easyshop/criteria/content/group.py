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
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IGroupCriteria
from Products.EasyShop.interfaces import IGroupManagement
from Products.EasyShop.interfaces import IItemManagement

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
        name='groups',
        widget=MultiSelectionWidget(
            label='Groups',
            label_msgid='schema_groups_label',
            i18n_domain='EasyShop',
        ),
        multiValued=1,
        vocabulary="_getGroupsAsDL"
    ),

),
)

class GroupCriteria(BaseContent):
    """
    """
    implements(IGroupCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Groups"

    def getValue(self):
        """
        """
        return ", ".join(self.getGroups())
                
    def _getGroupsAsDL(self):
        """Returns all Categories as DisplayList
        """

        dl = DisplayList()
        catalog = getToolByName(self, "portal_catalog")

        for group in catalog.searchResults(portal_type="EasyShopGroup"):
            dl.add(group.id, group.Title)

        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id"""

        transaction.commit()
        new_id = "GroupCriteria"
        self.setId(new_id)

registerType(GroupCriteria, PROJECTNAME)