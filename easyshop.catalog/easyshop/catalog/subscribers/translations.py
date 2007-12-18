# CMFCore imports
from Products.CMFCore.utils import getToolByName

def syncCategoryTranslations(category, event):
    """
    """
    # Establish product/category link between translations, based on canonical 
    # category
    ltool = getToolByName(category, "portal_languages")
    default_language = ltool.getDefaultLanguage()
    
    # If the given category is the canonical object, update all translations
    # of this category.
    
    if category.isCanonical():
        for canonical_product in category.getProducts():
            for language in ltool.getAvailableLanguages():
                translated_category = category.getTranslation(language)
                translated_product  = canonical_product.getTranslation(language)
                if translated_product and translated_category:
                    translated_category.addReference(translated_product, "categories_products")
                    
    # Otherwise we just update the modified translation (This happens only if
    # a translation is initialized)
                        
    else:                
        canonical_category = category.getCanonical()
        if canonical_category is None:
            return
            
        for canonical_product in canonical_category.getProducts():
            translated_category = canonical_category.getTranslation()
            translated_product  = canonical_product.getTranslation()
            if translated_product and translated_category:
                translated_category.addReference(translated_product, "categories_products")

def syncProductTranslations(product, event):
    """
    """
    # Establish product/category link between translations, based on canonical 
    # product
    ltool = getToolByName(product, "portal_languages")
    
    canonical_product = product.getCanonical()
    canonical_language = canonical_product.getLanguage()
                    
    for canonical_category in canonical_product.getBRefs("categories_products"):
        for language in ltool.getAvailableLanguages():
            translated_category = canonical_category.getTranslation(language)
            if translated_category is not None:
                product.addReference(translated_category, "categories_products")
                
