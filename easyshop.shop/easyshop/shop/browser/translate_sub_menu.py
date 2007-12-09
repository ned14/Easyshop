from zope.interface import implements
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from Products.LinguaPlone import LinguaPloneMessageFactory as _
from Products.LinguaPlone.browser.interfaces import ITranslateSubMenuItem

# NOTE: Overrides LinguaPlone's translate menu to hide it for IShop content 
# items, which are translatable by default (as they are ATFolders)
 
class TranslateSubMenuItem(BrowserSubMenuItem):    
    implements(ITranslateSubMenuItem)

    title = _(u"label_translate_menu", default=u"Translate into...")
    description = _(u"title_translate_menu",
            default="Manage translations for your content.")
    submenuId = "plone_contentmenu_translate"

    order = 5
    extra = { "id" : "plone-contentmenu-translate" }

    @property
    def action(self):
        return self.context.absolute_url() + "/manage_translations_form"

    def available(self):
        return False

    def disabled(self):
        return False

    def selected(self):
        return False
