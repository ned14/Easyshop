# zope imports
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

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
        
addressFactory = Factory(Address, title=_(u"Create a new address"))