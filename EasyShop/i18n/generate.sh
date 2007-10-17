#!/bin/sh

i18ndude rebuild-pot --pot easyshop.pot --create EasyShop --merge extra.pot\
    ../skins/easyshop_checkout\
    ../skins/easyshop_macros\
    ../skins/easyshop_mail_templates\
    ../skins/easyshop_manage\
    ../skins/easyshop_portlets\
    ../skins/easyshop_templates\
    ../browser

i18ndude sync --pot easyshop.pot easyshop-de.po
i18ndude sync --pot easyshop-schema.pot easyshop-schema-de.po
i18ndude sync --pot easyshop-plone.pot easyshop-plone-de.po