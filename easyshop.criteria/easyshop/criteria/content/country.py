# zope imports
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
from Products.EasyShop.interfaces import ICountryCriteria
from Products.EasyShop.interfaces import IShopManagement

schema = Schema((

    LinesField(
        name='countries',
        multiValued=1,
        vocabulary="_getCountriesAsDL",        
        widget=MultiSelectionWidget(
            label='Countries',
            label_msgid='schema_value_label',
            i18n_domain='EasyShop',
        ),
    ),
    
),
)

class CountryCriteria(BaseContent):
    """
    """
    implements(ICountryCriteria)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Country"
        
    def getValue(self):
        """
        """
        return ", ".join(self.getCountries())
    
    def _getCountriesAsDL(self):
        """
        """
        dl = DisplayList()
        for country in IShopManagement(self.context).getShop().getCountries():
            dl.add(country, country)

        return dl
        
registerType(CountryCriteria, PROJECTNAME)
