# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMF imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IGroupManagement
from Products.EasyShop.interfaces import IProductContent
from Products.EasyShop.interfaces import IPropertyManagement
from Products.EasyShop.interfaces import ITaxes

class ProductPropertyManagement:
    """Provides IPropertyManagement for product content objects.
    """
    implements(IPropertyManagement)
    adapts(IProductContent)

    def __init__(self, context):
        """
        """
        self.context = context

    def getPriceForCustomer(self, property_id, option_name):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        tax_rate = ITaxes(self.context).getTaxRateForCustomer()
        
        price_net = self.getPriceNet(property_id, option_name)
        price_for_customer =  price_net * ((tax_rate + 100) / 100)

        return price_for_customer
        
    def getPriceGross(self, property_id, option_name):
        """
        """
        found = False
        for property in self.getProperties():
            if property.getId() == property_id:
                found = True
                break

        if found == False:
            return 0.0
                    
        found = False
        for option in property.getOptions():
            if option["name"] == option_name:
                found = True
                break
                
        if found == False:
            return 0.0
                    
        try:
            price = float(option["price"])
        except ValueError:
            price = 0.0

        return price
        
    def getPriceNet(self, property_id, option_name):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        tax_rate = ITaxes(self.context).getTaxRate()
        
        price_gross = self.getPriceGross(property_id, option_name)     
        price_net =  price_gross / ((100 + tax_rate) / 100)
        
        return price_net
        
    def getProperties(self):
        """Returns all Properties for a Product.
                
           Properties from the Product have higher precedence than Properties
           from a Group.
        """
        groups = IGroupManagement(self.context).getGroups()

        # Get all Properties from Groups
        result = {}
        for group in groups:
            for property in group.objectValues("ProductProperty"):
                result[property.getId()] = property
        
        # Overwrite with Properties from Product
        for property in self.context.objectValues("ProductProperty"):
            result[property.getId()] = property
            
        return result.values()

    def getProperty(self, id):
        """
        """
        # Todo: Optimize
        for property in self.getProperties():
            if property.getId() == id:
                return property
        
        return None