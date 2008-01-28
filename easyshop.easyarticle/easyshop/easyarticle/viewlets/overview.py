# zope imports
from zope.component import getMultiAdapter

# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# Easyshop imports
from easyshop.core.interfaces import IFormats

class ContentViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('overview.pt')

    def __init__(self, context, request, view, manager):
        """
        """
        super(ContentViewlet, self).__init__(context, request, view, manager)
        self.article_view = getMultiAdapter(
            (self.context, self.request), name="article_view")

    @memoize
    def getFormats(self):
        """
        """
        return IFormats(self.context).getFormats()
    
    def getProducts(self):
        """Returns list of list of products.
        """        
        f = self.getFormats()
        products_per_line = f.get("products_per_line")
        
        lines = []
        line  = []
        for i, product in enumerate(self.article_view.getObjects()):
            line.append(product)

            # CSS Class    
            if (i + 1) % products_per_line == 0:
                klass = "last"
            else:
                klass = "notlast"
            
            # NOTE: "klass"-key is overwritten here as the product has already a
            # default klass.
            product["klass"] = klass

            # image
            if product["image_url"] is not None:
                product["image_url"] = "%s/image_%s" % (product["image_url"], f.get("image_size"))
                        
            if (i+1) % products_per_line == 0:
                lines.append(line)
                line = []
                
        if len(line) > 0:
            lines.append(line)
            
        return lines

    @memoize        
    def showEditFunctions(self):
        """
        """
        return self.article_view.showEditFunctions()        

    @memoize
    def getTdWidth(self):
        """
        """
        return "%s%%" % (100 / self.getFormats().get("products_per_line"))