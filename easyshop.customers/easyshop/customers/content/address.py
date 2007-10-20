# zope imports
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.interfaces import IAddress
from Products.EasyShop.config import *

schema = Schema((

    StringField(
        name='firstname',
        required=1,
        widget=StringWidget(
            label='First Name',
            label_msgid='schema_firstname_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='lastname',
        required=1,
        widget=StringWidget(
            label='Last Name',
            label_msgid='schema_lastname_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='companyName',
        widget=StringWidget(
            label='Company Name',
            label_msgid='schema_companyname_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='address1',
        required=1,        
        widget=StringWidget(
            label='Address 1',
            label_msgid='schema_address1_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='address2',
        widget=StringWidget(
            label='Address 2',
            label_msgid='schema_address2_label',
            i18n_domain='EasyShop',
        )
    ),

    StringField(
        name='zipCode',
        required=1,        
        widget=StringWidget(
            label='Zip Code',
            label_msgid='schema_zipcode_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='city',
        required=1,        
        widget=StringWidget(
            label='City',
            label_msgid='schema_city_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='country',
        required=1,
        vocabulary="_getCountriesAsDL",
        default="Deutschland",
        widget=SelectionWidget(
            label='Country',
            label_msgid='schema_country_label',
            i18n_domain='EasyShop',
        ),
    ),

    StringField(
        name='phone',
        required=1,        
        widget=StringWidget(
            label='Phone',
            label_msgid='schema_phone_label',
            i18n_domain='EasyShop',
        ),
    ),

),
)

Address_schema = BaseSchema.copy() + schema.copy()
Address_schema["title"].widget.visible = {'view':'invisible', 'edit':'invisible'}
Address_schema["title"].required = 0

class Address(BaseContent):
    """
    """
    implements(IAddress)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = Address_schema

    def Title(self):
        """
        """
        return self.getName()
        
    def getName(self, reverse=False):
        """
        """
        if reverse:
            name = self.getLastname()
            if name != "": name += ", "
            name += self.getFirstname()

        else:
            name = self.getFirstname()
            if name != "": name += " "
            name += self.getLastname()
        
        return name
        
    def _getCountriesAsDL(self):
        """
        """
        dl = DisplayList()
        
        countries = self.getShop().getCountries()

        for country in countries:
            dl.add(country, country)
            
        return dl
        
registerType(Address, PROJECTNAME)