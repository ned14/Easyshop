# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import TEXTS, IMAGE_SIZES
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IShop


class IFormatterPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IFormatterPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Formatter")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('formatter.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if not mtool.checkPermission("Manage portal", self.context):
            return False
             
        if (ICategory.providedBy(self.context) or \
            IShop.providedBy(self.context)) == False:
            return False

        return True        

    @memoize
    def getFormatInfo(self):
        """
        """
        fi = IFormats(self.context)
        return fi.getFormats(effective=False)

    def getTexts(self):
        """
        """
        fi = self.getFormatInfo()
        selected_text = fi["text"]
        
        result = []
        for text in TEXTS:        
            result.append({
                "id" : text[0],
                "title" : text[1],
                "selected" : selected_text == text[0],
            })
    
        return result
        
    def getImageSizes(self):
        """
        """
        fi = self.getFormatInfo()
        selected_size = fi["image_size"]
        
        sizes = IMAGE_SIZES.keys()
        sizes.sort(lambda a, b: cmp(IMAGE_SIZES[a][0], IMAGE_SIZES[b][0]))

        result = []
        for size in sizes:
            result.append({
                "title" : size,
                "selected" : selected_size == size,
            })
            
        return result

class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()

class FormatterView(BrowserView):
    """
    """
    def saveFormatter(self):
        """
        """
        fi = IFormats(self.context)
        f = fi.setFormats(self.request)
                
        referer = self.request.get("HTTP_REFERER", "")
        if referer.find("thank-you") != -1:
            url = referer
        else:
            url = self.context.absolute_url()
                            
        self.request.response.redirect(url)