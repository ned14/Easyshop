# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IProductVariants
from easyshop.core.interfaces import IProductVariantsManagement

class ProductVariantsManagement:
    """Provides IProductVariantsManagement for product content objects.
    """
    implements(IProductVariantsManagement)
    adapts(IProductVariants)

    def __init__(self, context):
        """
        """
        self.context = context

    def addVariant(self, title, properties):
        """
        """
        new_id = self.context.generateUniqueId("ProductVariant")
        self.context.invokeFactory(
            "ProductVariant", id=new_id, title=title, forProperties=properties)
        
        return id
            
    def getDefaultVariant(self):
        """
        """
        try:        
            return self.getVariants()[0]
        except IndexError:
            return None
                
    def getVariants(self):
        """
        """
        return self.context.objectValues("ProductVariant")

    def getSelectedVariant(self, selected_properties=None):
        """
        """
        if selected_properties is None:
            selected_properties = {}
            for name, value in self.context.REQUEST.items():
                if name.startswith("property"):
                    selected_properties[name[9:]] = value

        result = []
        for key, value in selected_properties.items():
            result.append("%s:%s" % (key, value))
            
        result.sort()
        result = "|".join(result)
        
        for variant in self.context.objectValues("ProductVariant"):
            for_properties = list(variant.getForProperties())
            for_properties.sort()
            for_properties = "|".join(for_properties)
            
            if result.lower() == for_properties.lower():
                return variant

        return self.getDefaultVariant()