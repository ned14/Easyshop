from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles

class HiddenProducts(object):
    """
    """
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return [
            u'easyshop.carts',
            u'easyshop.catalog',
            u'easyshop.criteria',
            u'easyshop.customers',
            u'easyshop.discounts',
            u'easyshop.groups',
            u'easyshop.information',            
            u'easyshop.kss',
            u'easyshop.login',
            u'easyshop.management',
            u'easyshop.order',
            u'easyshop.payment',
            u'easyshop.shipping',
            u'easyshop.shop',
            u'easyshop.stocks',
            u'easyshop.taxes',            
        ]