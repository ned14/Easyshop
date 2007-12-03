# EasyArticle imports 
from Products.EasyArticle.browser.article import ArticleView

class ProductsView(ArticleView):
    """
    """
    def getProducts(self):
        """Returns list of list of products.
        """        
        lines = []
        line  = []
        for i, product in enumerate(self.getObjects()):
            line.append(product)
            
            if (i+1) % 2 == 0:
                lines.append(line)
                line = []
                
        if len(line) > 0:
            lines.append(line)
            
        return lines