# CMFCore imports
from Products.CMFCore.utils import getToolByName

def syncCategoryTranslations(category, event):
    """This is called after init and after edit.
    """
    ltool = getToolByName(category, "portal_languages")
    default_language = ltool.getDefaultLanguage()
    
    # If the given category is the canonical object, update all translations
    # of this category. This must happend for edit and init.
    # 1. Init: All possible before existing translations get the links from the
    #          canonical object.
    # 2. Edit: After change of links the translations have to be updated.
    
    if category.isCanonical():
        for language in ltool.getSupportedLanguages():
            if language == ltool.getDefaultLanguage():
                continue
            translated_category = category.getTranslation(language)
            translated_category.deleteReferences("categories_products")
            for canonical_product in category.getProducts():
                translated_product = canonical_product.getTranslation(language)
                if translated_product and translated_category:                    
                    translated_category.addReference(translated_product, "categories_products")
                    
    # Otherwise we just update the initialized translation (but I leave it 
    # although here for simplicity). After a translation is initialized all
    # already existing links are overtaken. Later links cannot changed via
    # translation but only via canonical object, so no update is neccessary.
    else:                
        canonical_category = category.getCanonical()
        if canonical_category is None:
            return
            
        for canonical_product in canonical_category.getProducts():
            translated_product = canonical_product.getTranslation()
            if translated_product:
                category.addReference(translated_product, "categories_products")

def syncProductTranslations(product, event):
    """
    """
    for category in product.getBRefs("categories_products"):
        syncCategoryTranslations(category, event)