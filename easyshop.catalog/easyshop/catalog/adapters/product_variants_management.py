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
        
    def getDefaultProductVariant(self):
        """
        """
        try:        
            return self.getProductVariants()[0]
        except IndexError:
            return None
                
    def getProductVariants(self):
        """
        """
        return self.context.objectValues("ProductVariant")

    def getSelectedProductVariant(self, selected_properties=None):
        """
        """
        if selected_properties is None:
            selected_properties = {}
            for name, value in self.context.REQUEST.form.items():
                if name.startswith("property"):
                    selected_properties[name[9:]] = value

        result = []
        for key, value in selected_properties.items():
            result.append("%s:%s" % (key.lower(), value.lower()))
            
        result = "|".join(result)
        
        for variant in self.context.objectValues("ProductVariant"):
            if result == variant.getForProperties():
                return variant

        return self.getDefaultProductVariant()