# zope imports
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

# easyshop imports
from easyshop.core.interfaces import IShopManagement

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

def countries(context):
    """
    """
    terms = []
    for country in IShopManagement(context).getShop().getCountries():
        terms.append(SimpleTerm(country, country))    
    return SimpleVocabulary(terms)