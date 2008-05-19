# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import ICategoriesContainer
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IShopManagement

class CategoriesViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('categories.pt')

    def getCategories(self):
        """
        """
        f = self.getFormats()
        products_per_line = f.get("products_per_line")

        cm = ICategoryManagement(self.context)

        line  = []
        lines = []
        for i, category in enumerate(cm.getTopLevelCategories()):

            category = category.getObject()

            # Image
            if len(category.getImage()) != 0:
                image_url = "%s/image_%s" % \
                    (category.absolute_url(), f.get("image_size"))
            else:
                image_url = None

            # Text    
            temp = f.get("text")
            if temp == "description":
                text = category.getDescription()
            elif temp == "short_text":
                text = category.getShortText()
            elif temp == "text":
                text = category.getText()
            else:
                text = ""

            # CSS Class    
            if (i + 1) % products_per_line == 0:
                klass = "last"
            else:
                klass = "notlast"
                
            line.append({
                "title"     : category.Title(),
                "text"      : text, 
                "url"       : category.absolute_url(),
                "image_url" : image_url,
                "klass"     : klass,
            })
            
            if (i+1) % products_per_line == 0:
                lines.append(line)
                line = []
                
                            
        if len(line) > 0:
            lines.append(line)
            
        return lines

    @memoize
    def getBackToOverViewUrl(self):
        """
        """
        parent = self.context.aq_inner.aq_parent
        if ICategory.providedBy(parent):
            parent_url = parent.absolute_url()
        elif ICategoriesContainer.providedBy(parent):
            shop = IShopManagement(self.context).getShop()
            parent_url = shop.absolute_url()
        else:
            parent_url = None
            
        return parent_url
        
    @memoize
    def getFormats(self):
        """
        """
        # Could be overwritten to provide fixed category views.
        # s. DemmelhuberShop
        return IFormats(self.context).getFormats()
    
    @memoize
    def getTdWidth(self):
        """
        """
        return "%s%%" % (100 / self.getFormats().get("products_per_line"))