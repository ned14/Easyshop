# zope imports
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.component import adapter

# Archetypes imports
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IProductVariants
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IProperty

@adapter(IProperty, IObjectInitializedEvent)
def addProperty(property, event):
    """Adds the newly created property to all existing product variants.
    """
    product = property.aq_inner.aq_parent
    if IProductVariants.providedBy(product) == False:
        return 
    
    try:
        option = property.getOptions()[0]
    except IndexError:
        return
    
    option = "%s:%s" % (property.getId(), option["id"])
    for variant in IProductVariantsManagement(product).getVariants():
        properties = list(variant.getForProperties())
        properties.append(option)
        properties.sort()
        variant.setForProperties(properties)
        
@adapter(IProperty, IObjectRemovedEvent)
def deleteProperty(property, event):
    """Removes property from all existing product variants.
    """
    product = property.aq_inner.aq_parent
    if IProductVariants.providedBy(product) == False:
        return 
        
    to_delete_property_id = property.getId()
    for variant in IProductVariantsManagement(product).getVariants():
        new_properties = []
        for variant_property in variant.getForProperties():
            variant_property_id = variant_property.split(":")[0]
            if variant_property_id != to_delete_property_id:
                new_properties.append(variant_property)
        new_properties.sort()

        variant.setForProperties(new_properties)