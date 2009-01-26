# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

class CategoriesViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('categories.pt')

    def getInfo(self):
        """
        """
        ret = { 'title'         : self.context.Title(),
                'absolute_url'  : self.context.absolute_url()
              }
    
        return ret

    def getCategories(self):
        """
        """
        f = self.getFormats()
        products_per_line = f.get("products_per_line")

        cm = ICategoryManagement(self.context)

        line  = []
        lines = []
        for i, category in enumerate(cm.getTopLevelCategories()):

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

    def getShopURL(self):
        """
        """
        return IShopManagement(self.context).getShop().absolute_url()

    def getBreadCrumbs(self) :
        """
        """
        parents = []
        
        parent = self.context.getRefs("parent_category")
        
        while len(parent) > 0 :
          parent = ICategory(parent[0])
          parents.append({"title"   : parent.Title(),
                          "absolute_url"  : parent.absolute_url()
                         }
                        )                            
          parent = parent.getRefs("parent_category")

        parents.reverse()
        
        if len(parents) > 0 :
          parents[(len(parents)+(-1))] = {
                          "last"         : True,
                          "absolute_url" : parents[(len(parents)+(-1))]['absolute_url'],
                          "title"        : parents[(len(parents)+(-1))]['title']
                          }
        
        return parents


    @memoize
    def getBackToOverViewUrl(self):
        """
        """
        if IShop.providedBy(self.context):
            return None
        
        parent_category = self.context.getRefs("parent_category")
        if len(parent_category) > 0:
            return parent_category[0].absolute_url()

        shop = IShopManagement(self.context).getShop()
        return shop.absolute_url()
        
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