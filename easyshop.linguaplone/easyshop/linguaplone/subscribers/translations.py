# CMFCore imports
from Products.CMFCore.utils import getToolByName

def syncCategoryTranslations(category, event):
    """This is called after init and after edit.
    """
    syncRelations(category, "categories_products")
    
def syncProductTranslations(product, event):
    """This is called after init and after edit.
    """    
    ltool = getToolByName(product, "portal_languages")
    default_language = ltool.getDefaultLanguage()    

    ## Collect all affected categories
    
    # First we get the related categories of the modified product.
    categories = product.getCanonical().getBRefs("categories_products")
    
    # In case that a category has been deleted from the product we collect also
    # all categories of the first translation which is not canonical. With just
    # the approach above we would not get the category, hence they would not get
    # updated.
    
    for language in ltool.getSupportedLanguages():
        if language != default_language:
            translation = product.getTranslation(language)
            if translation is not None:
                break
    
    if translation is not None:
        for category in translation.getBRefs("categories_products"):
            if category not in categories:
                categories.append(category)
    
    for category in categories:
        syncRelations(category, "categories_products")
    
    syncRelations(product, "products_products")
    
def syncRelations(object, relation):
    """All translations of given object will have the same related objects for 
    given relation. Base is the canonical of the given object.
    """
    ltool = getToolByName(object, "portal_languages")
    default_language = ltool.getDefaultLanguage()
    
    canonical = object.getCanonical()
    
    for language in ltool.getSupportedLanguages():

        if language == ltool.getDefaultLanguage():
            continue

        translation = canonical.getTranslation(language)

        if translation is None:
            continue
            
        translation.deleteReferences(relation)
        
        for referenced_canonical in canonical.getRefs(relation):
            
            referenced_translation = referenced_canonical.getTranslation(language)
            
            if referenced_translation is not None:
                translation.addReference(referenced_translation, relation)
