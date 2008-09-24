#!/bin/sh

i18ndude rebuild-pot --pot easyshop.pot --create EasyShop --merge extra.pot\
    ../../../src/easyshop.carts\
    ../../../src/easyshop.catalog\
    ../../../src/easyshop.checkout\
    ../../../src/easyshop.core\
    ../../../src/easyshop.customers\
    ../../../src/easyshop.groups\
    ../../../src/easyshop.information\
    ../../../src/easyshop.io\
    ../../../src/easyshop.order\
    ../../../src/easyshop.payment\
    ../../../src/easyshop.shipping\
    ../../../src/easyshop.stocks\
    ../../../src/easyshop.shop

                                    
i18ndude sync --pot easyshop.pot easyshop-de.po
i18ndude sync --pot easyshop-schema.pot easyshop-schema-de.po
i18ndude sync --pot easyshop-plone.pot easyshop-plone-de.po