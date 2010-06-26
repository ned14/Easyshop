#!/bin/sh

i18ndude rebuild-pot --pot easyshop.pot --create EasyShop --merge extra.pot\
    ../../../src/easyshop.carts\
    ../../../src/easyshop.catalog\
    ../../../src/easyshop.checkout\
    ../../../src/easyshop.core\
    ../../../src/easyshop.criteria\
    ../../../src/easyshop.customers\
    ../../../src/easyshop.discounts\
    ../../../src/easyshop.groups\
    ../../../src/easyshop.information\
    ../../../src/easyshop.io\
    ../../../src/easyshop.login\
    ../../../src/easyshop.kss\
    ../../../src/easyshop.management\
    ../../../src/easyshop.order\
    ../../../src/easyshop.payment\
    ../../../src/easyshop.shipping\
    ../../../src/easyshop.stocks\
    ../../../src/easyshop.shop\
    ../../../src/easyshop.taxes\


i18ndude sync --pot easyshop.pot easyshop-de.po
i18ndude sync --pot easyshop-schema.pot easyshop-schema-de.po
i18ndude sync --pot easyshop-plone.pot easyshop-plone-de.po
