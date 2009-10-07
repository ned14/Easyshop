# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.component import queryUtility
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IVocabularyFactory

# plone imports
from plone.app.content.item import Item

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IAddress

class Address(Item):
    """
    """
    implements(IAddress)
    portal_type = "Address"

    firstname     = FieldProperty(IAddress["firstname"])
    lastname      = FieldProperty(IAddress["lastname"])
    company_name  = FieldProperty(IAddress["company_name"])
    address_1     = FieldProperty(IAddress["address_1"])
    zip_code      = FieldProperty(IAddress["zip_code"])
    city          = FieldProperty(IAddress["city"])
    country       = FieldProperty(IAddress["country"])
    phone         = FieldProperty(IAddress["phone"])
    email         = FieldProperty(IAddress["email"])

    country = u""

    def Title(self):
        """
        """
        return self.getName()

    def getName(self, reverse=False):
        """
        """
        if reverse:
            name = self.lastname
            if name != "": name += ", "
            name += self.firstname
        else:
            name = self.firstname
            if name != "": name += " "
            name += self.lastname

        return name

    def country_title(self):
        """
        """
        vocab = queryUtility(IVocabularyFactory, name="easyshop.countries")
        try:
            country = vocab(self).getTerm(self.country)
            return country.title
        except:
            # country was not found in vocab. happens sometimes
            # if ES is updated from old revision to r1634 or newer
            return self.country


addressFactory = Factory(Address, title=_(u"Create a new address"))