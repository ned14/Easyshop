# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.Archetypes.interfaces import IObjectEditedEvent

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategory

def syncCategoryTranslations(category, event):
    """
    """
    # Establish product/category link between translations, based on canonical 
    # category
    ltool = getToolByName(category, "portal_languages")
    
    canonical_category = category.getCanonical()
    canonical_language = canonical_category.getLanguage()

    import pdb; pdb.set_trace()
    for canonical_product in canonical_category.getProducts():
        for language in ltool.getAvailableLanguages():
            translated_category = canonical_category.getTranslation(language)
            translated_product  = canonical_product.getTranslation(language)
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
                
