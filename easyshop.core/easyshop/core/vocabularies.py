# zope imports
from zope.component import queryUtility
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

# easyshop imports
from easyshop.core.interfaces import IShopManagement

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer.interfaces import IIDNormalizer

def countries(context):
    """
    """
    terms = []
    # terms.append(SimpleTerm("Germany", u"Germany"))
    # terms.append(SimpleTerm("USA", u"USA"))
    # terms.append(SimpleTerm("Polen", u"Polen"))

    for country in IShopManagement(context).getShop().getCountries():
        country = safe_unicode(country)
        term_value = queryUtility(IIDNormalizer).normalize(country)
        terms.append(SimpleTerm(term_value, term_value, country))

    return SimpleVocabulary(terms)