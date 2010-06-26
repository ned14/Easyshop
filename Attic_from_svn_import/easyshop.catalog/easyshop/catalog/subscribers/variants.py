# zope imports
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.component import adapter

# easyshop imports
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IProperty
from easyshop.core.interfaces import IPropertyOption

@adapter(IProperty, IObjectRemovedEvent)
def deleteProperty(property, event):
    """Removes property from all existing product variants.
    """
    product = property.aq_inner.aq_parent
    pvm = IProductVariantsManagement(product)
    
    if pvm.hasVariants() == False:
        return 
        
    to_delete_property_id = property.getId()
    for variant in pvm.getVariants():
        new_properties = []
        for variant_property in variant.getForProperties():
            variant_property_id = variant_property.split(":")[0]
            if variant_property_id != to_delete_property_id:
                new_properties.append(variant_property)
        new_properties.sort()

        variant.setForProperties(new_properties)
        
@adapter(IPropertyOption, IObjectRemovedEvent)
def deleteProperty(option, event):
    """Removes property from all existing product variants.
    """
    property = option.aq_inner.aq_parent
    if property.getOptions() == 0:
        deleteProperty(property, event)