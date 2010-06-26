# zope imports
from zope.component import queryUtility
from zope.component import getSiteManager
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

    shop = IShopManagement(context).getShop()

    if shop is None:
        # BBB: this is ugly because if we create a new address
        #      we dont have any context. try to guess the first EasyShop
        #      in portal_catalog and hope we are in luck!
        # XXX: this breaks if the site has more than one EasyShop instances!!!
        sm = getSiteManager()
        cat_query = sm.portal_catalog.queryCatalog(
            dict(portal_type='EasyShop'))

        if len(cat_query)<1:
            # this is not possible, because we weren't in this vocab if
            # we hadn't an EasyShop instance
            __traceback_info__ = "no Easyshop found in portal_catalog"
            raise Exception

        shop = cat_query[0].getObject()

    for country in shop.getCountries():
        country = safe_unicode(country)
        term_value = queryUtility(IIDNormalizer).normalize(country)
        terms.append(SimpleTerm(term_value, term_value, country))

    return SimpleVocabulary(terms)